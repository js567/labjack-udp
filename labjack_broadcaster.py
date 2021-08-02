"""
LabJack UDP Broadcast Script - Object-Oriented V0.3.1

Code by Jack Stevenson and Chris Romsos, referencing code from LabJack Corporation

Creates LabJack class to instantiate a LabJack object for broadcasting. This script can be imported to another for use
as a module. The class has a number of methods that can be called in this script or in a separate one if imported as
a module.

For more information or to view the latest version of this script, visit https://github.com/cromsos/CORIOLIX_labjack
"""
# Update ideas: new socket number for each input

from labjack import ljm
import datetime
# import os
# import sys
# import time
import socket
from threading import Thread


# Sensor class which is added to LabJack object to gather data over UDP
class Sensor:
    def __init__(self, pin="AIN0", port="30325", rate=1000, name="sensor", number=0):
        self._pin = pin
        self._port = port
        self._rate = rate
        self._name = name
        self._intervalHandle = 0
        self._number = number

    def set_port(self, port):
        """ Sets port name (default is 30325). """
        self._port = port

    def get_port(self):
        """ Returns port name (default is 30325). """
        return self._port

    def set_pin(self, pin):
        """ Sets pin number (default is AIN0). """
        self._pin = pin

    def get_pin(self):
        """ Returns pin number (default is AIN0). """
        return self._pin

    def set_frequency_ms(self, frequency):
        """ Sets upload frequency in milliseconds (default is 1000 ms). """
        self._rate = frequency

    def set_frequency_hz(self, frequency):
        """ Sets upload frequency in hertz (default is 1 Hz). """
        self._rate = (1/frequency) * 1000

    def get_rate(self):
        """ Returns sampling rate (default is 1000 ms)."""
        return self._rate

    def get_name(self):
        """ Returns sensor name. """
        return self._name

    def set_number(self, number):
        """ Set number for interval tracking - not meant to be set manually """
        self._number = number

    def get_number(self):
        """ Get number for use in interval - not meant to be set manually """
        return self._number


# LabJack class with custom methods
class LabJack:

    """ Initializes all critical processes for LabJack network connection and data transfer. """
    def __init__(self, connection="ETHERNET", serial_number="470025307"):

        self._connection = connection
        self._serial_number = serial_number
        self._sensors = []
        self._num_sensors = 0  # Number of sensors connected to the LabJack
        self._interval_number = 0  # Auto-assigned ID for a sensor that associates it with an interval for threading

        print("Trying to find LabJack...")

        # LabJack Connection - DATA IN
        # Open the LabJack serial number 470025307 on IP connection.
        try:
            self._handle = ljm.openS("T7", connection, serial_number)  # T7 device, IP connection, SN
            print("LabJack found and connected over: " + connection)

        except ljm.LJMError:
            print("""
            LabJack not found. Make sure connection method is correct (Ethernet or USB) and network is correct.
            Connection method can be set when initializing LabJack object - ex. LJ = LabJack(connection="USB")
            Default connection is Ethernet.
            """)
            exit()

        # Get the connection metadata
        info = ljm.getHandleInfo(self._handle)
        print("\nOpened a LabJack with Device type: %i, Connection type: %i,\n"
              "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
              (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

        # UDP Socket - DATA OUT
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # need to clean up this method, it has some potential weak spots
    def add(self, sensor):
        """ Adds a sensor to LabJack object. """
        sensor.set_number(self._interval_number)
        self._sensors.append(sensor)
        self._num_sensors += 1
        self._interval_number += 1

    # Potentially problematic implementation - check functionality
    def remove(self, name):
        """ Removes a sensor from LabJack object. """
        if self._sensors == []:
            print("Sensor list blank - couldn't find a sensor to remove.")
            return
        for item in self._sensors:
            if item.get_name() == name:
                self._sensors.remove(item)
                self._num_sensors -= 1

    def clear(self):
        """ Removes all sensors from LabJack object. """
        self._sensors.clear()
        self._num_sensors = 0
        return

    def sensor_broadcast(self, sensor):
        """ Broadcast method for sensors for multithreading - don't call this explicitly. """

        # Prepare final variables for program execution
        rateus = sensor.get_rate() * 1000
        ljm.startInterval(sensor.get_number(), rateus)

        last_tick = ljm.getHostTick()

        while True:

            try:

                ljm.waitForNextInterval(sensor.get_number())
                cur_tick = ljm.getHostTick()
                duration = (cur_tick - last_tick) / 1000
                cur_time = datetime.datetime.now()
                cur_time_str = cur_time.isoformat(timespec='milliseconds')

                result = ljm.eReadName(self._handle, sensor.get_pin())

                message = f"{cur_time_str}, {sensor.get_name()}, {sensor.get_rate()}, {duration}, {result}"
                print(message)

                print("Sending UDP")
                self._sock.sendto(bytes(message, "utf-8"), ("255.255.255.255", int(sensor.get_port())))
                print("Sending Done")

                # Set lastTick equal to curTick
                last_tick = cur_tick

            except ljm.LJMError:
                print("LabJack not found")
                break

            except KeyboardInterrupt:
                break

            except Exception:
                import sys
                print(sys.exc_info()[1])
                break

        print("\nFinished!")

        # Get the final time
        app_end_time = datetime.datetime.now()
        end_time_str = app_end_time.isoformat(timespec='milliseconds')
        print("The final time is: %s" % end_time_str)

        # Close fi
        # Close handles
        ljm.cleanInterval(0)
        ljm.close(self._handle)

    def start_broadcast(self):
        """ Begin broadcasting over UDP. """

        # Get the current time to build a time-stamp.
        app_start_time = datetime.datetime.now()
        start_time_str = app_start_time.isoformat(timespec='milliseconds')
        # time_str = app_start_time.isoformat(timespec='milliseconds')

        # Print some program-initialization information
        print("The time is: %s" % start_time_str)

        threads = []
        for sensor in self._sensors:

            t = Thread(target=self.sensor_broadcast, args=(sensor, ))
            threads.append(t)
            t.start()

        print(self._sensors)
        print(threads)

        for thread in threads:
            thread.join()

    def stop_broadcast(self):

        print("\nFinished!")

        raise KeyboardInterrupt

        # Get the final time
        app_end_time = datetime.datetime.now()
        end_time_str = app_end_time.isoformat(timespec='milliseconds')
        print("The final time is: %s" % end_time_str)

        # Close fi
        # Close handles
        ljm.cleanInterval(0)
        ljm.close(self._handle)

        return 0


if __name__ == '__main__':
    Jack = LabJack()
    WaterSensor = Sensor("AIN0", name="WaterSensor", rate=500)
    MainSensor = Sensor("AIN1", name="MainSensor", rate=1000)
    Jack.add(WaterSensor)
    Jack.add(MainSensor)

    Jack.start_broadcast()
