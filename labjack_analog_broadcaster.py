"""
This example is meant to be paired with LabJack's other examples:
https://labjack.com/support/software/examples/ljm/python
This example demonstrates reading a single analog input (AIN0)
from a LabJack (looping forever) and sampling at 10Hz or with a
100ms delay between samples).  Samples are logged to a .csv file
and UDP broadcast.

Docs for datetime: https://docs.python.org/3/library/datetime.html
A few relevant stackoverflow examples:
https://stackoverflow.com/questions/3316882/how-do-i-get-a-string-format-of-the-current-date-time-in-python
Docs for os (how to get the CWD):
https://docs.python.org/3/library/os.html
Docs for os.path (how to join paths):
https://docs.python.org/3/library/os.path.html#module-os.path
"""

from labjack import ljm
import datetime
import os
import sys
import time
import socket

# Labjack Connection - DATA IN
# Open the LabJack serial number 470025307 on IP connection.
handle = ljm.openS("T7", "ETHERNET", "470025307")  # T7 device, IP connection, SN

# Get the connection metadata
info = ljm.getHandleInfo(handle)
print("\nOpened a LabJack with Device type: %i, Connection type: %i,\n"
      "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
      (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

# UDP Socket - DATA OUT
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Setup and call eReadName to read from AIN1 on the LabJack.
name = "AIN1"
rate = 1000  # in ms
rateUS = rate*1000

# Get the current time to build a time-stamp.
appStartTime = datetime.datetime.now()
startTimeStr = appStartTime.isoformat(timespec='milliseconds')
timeStr = appStartTime.isoformat(timespec='milliseconds')

print(timeStr)

# # Get the current working directory
# cwd = os.getcwd()

# # Build a file-name and the file path.
# fileNameColon = timeStr + "-%s-Example.csv" % name
# c1 = 13
# c2 = 16
# newDelimiter = '.'
# fileName = fileNameColon[0:c1] + newDelimiter + fileNameColon[c1+1:c2] + newDelimiter + fileNameColon[c2+1: ]
# filePath = os.path.join(cwd, fileName)
# print(fileName + filePath)

# with open(fileName, 'w', newline='') as file:
#       writer = csv.writer(file)


# # Open the file & write a header-line
# f = open(filePath, 'w')
# f.writerow("Time Stamp, Duration/Jitter (ms), %s\n" % name)
# f.write("hello there")

# Print some program-initialization information
print("The time is: %s" % startTimeStr)

# Prepare final variables for program execution
intervalHandle = 0
ljm.startInterval(intervalHandle, rateUS)
numSkippedIntervals = 0

lastTick = ljm.getHostTick()
duration = 0

while True:
    try:
        numSkippedIntervals = ljm.waitForNextInterval(intervalHandle)
        curTick = ljm.getHostTick()
        duration = (curTick-lastTick)/1000
        curTime = datetime.datetime.now()
        curTimeStr = curTime.isoformat(timespec='milliseconds')

        # Read AIN0
        result = ljm.eReadName(handle, name)
        # f.write("%s, %0.1f, %0.3f\r\n" % (curTimeStr, duration, result))
        #
        print(f"{curTimeStr}, {duration}, {result}")

        message = "%s, %0.1f, %0.3f\r\n" % (curTimeStr, duration, result)
        #message = f"{curTimeStr}, {duration}, {result}"

        print("Sending UDP")
        sock.sendto(bytes(message, "utf-8"), ("255.255.255.255", 30325))
        print("Sending Done")

        # Set lastTick equal to curTick
        lastTick = curTick

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
ljm.cleanInterval(intervalHandle)
ljm.close(handle)
