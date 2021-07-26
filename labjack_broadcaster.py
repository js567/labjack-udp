"""
LabJack UDP Broadcast Script - Object-Oriented V0.0

Code by Jack Stevenson and Chris Romsos, referencing code from LabJack Corporation

Creates LabJack class to instantiate a LabJack object for broadcasting. This script can be imported to another for use
as a module. The class has a number of methods that can be called in this script or in a separate one if imported as
a module.

For more information or to view the latest version of this script, visit https://github.com/cromsos/CORIOLIX_labjack
"""
# Update ideas: new socket number for each input

from labjack import ljm
import datetime
import os
import sys
import time
import socket


# Custom error for use in upload issues
class UploadError(TypeError):
    pass


# LabJack class with custom methods
class LabJack:

    """ Initializes all critical processes for LabJack network connection and data transfer. """
    def __init__(self, connection="ETHERNET", serial_number="470025307"):

        self._connection = connection
        self._serial_number = serial_number
        self._names = ["AIN0"]

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

        # UDP Socket - DATA OUT
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._socket_number = 30325

        # Get the connection metadata
        info = ljm.getHandleInfo(self._handle)
        print("\nOpened a LabJack with Device type: %i, Connection type: %i,\n"
              "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
              (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

        # Setup and call eReadName to read from AIN1 on the LabJack.
        self._name = "AIN1"
        self._rate = 1000  # in ms
        self._rateus = self._rate * 1000  # in us (microseconds)

        # Set interval handle
        self._intervalHandle = 0

    def set_ports(self, ports):
        """ Sets which ports will be used for data output (default is AIN0). """

        # Clear current list of ports
        self._names.clear()

        # Add new ports to list of ports
        for port in ports:
            self._names.append(port)

    def set_frequency_ms(self, frequency):
        """ Sets upload frequency in milliseconds (default is 1000 ms). """
        self._rate = frequency

    def set_frequency_hz(self, frequency):
        """ Sets upload frequency in hertz (default is 1 Hz). """
        self._rate = (1/frequency) * 1000

    def set_socket_number(self, socket_number):
        """ Sets socket number (default is 30325). """
        self._socket_number = socket_number

    def start_broadcast(self):
        """ Begin broadcast over UDP. """

        # Get the current time to build a time-stamp.
        app_start_time = datetime.datetime.now()
        start_time_str = app_start_time.isoformat(timespec='milliseconds')
        time_str = app_start_time.isoformat(timespec='milliseconds')

        print(time_str)

        # Print some program-initialization information
        print("The time is: %s" % start_time_str)

        # Prepare final variables for program execution
        self._rateus = self._rate * 1000
        ljm.startInterval(self._intervalHandle, self._rateus)
        self._numSkippedIntervals = 0

        self._last_tick = ljm.getHostTick()

        while True:

            try:

                duration = 0

                self._numSkippedIntervals = ljm.waitForNextInterval(self._intervalHandle)
                self._cur_tick = ljm.getHostTick()
                duration = (self._cur_tick - self._last_tick)/1000
                cur_time = datetime.datetime.now()
                cur_time_str = cur_time.isoformat(timespec='milliseconds')

                print(self._rate)

                for name in self._names:
                    # Read AIN0
                    result = ljm.eReadName(self._handle, name)

                    message = f"{cur_time_str}, {duration}, {result}"
                    print(message)

                    print("Sending UDP")
                    self._sock.sendto(bytes(message, "utf-8"), ("255.255.255.255", self._socket_number))
                    print("Sending Done")

                # Set lastTick equal to curTick
                self._last_tick = self._cur_tick

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
        appEndTime = datetime.datetime.now()
        endTimeStr = appEndTime.isoformat(timespec='milliseconds')
        print("The final time is: %s" % endTimeStr)

        # Close fi
        # Close handles
        ljm.cleanInterval(self._intervalHandle)
        ljm.close(self._handle)

    def stop_upload(self):

        print("\nFinished!")

        # Get the final time
        appEndTime = datetime.datetime.now()
        endTimeStr = appEndTime.isoformat(timespec='milliseconds')
        print("The final time is: %s" % endTimeStr)

        # Close fi
        # Close handles
        ljm.cleanInterval(self._intervalHandle)
        ljm.close(self._handle)

        return 0


if __name__ == '__main__':
    Jack = LabJack()
    Jack.start_broadcast()
