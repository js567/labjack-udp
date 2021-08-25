"""
LabJack UDP Receiver Script
Object-Oriented V1.3 - Added threading support for multiple sensor output

Code by Jack Stevenson and Chris Romsos

This is a simple UDP receiving script to display data being returned from the LabJack. It does not save the data, so
you have to add a data collection scheme appropriate for your application, such as saving to a CSV file.

For more information or to view the latest version of this script, visit https://github.com/cromsos/CORIOLIX_labjack
"""
import socket

# Change to whatever port you are using for broadcast
port = 30325

# Create receiving socket
a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
a.bind(("", port))

# Print message if connected to port but not receiving data yet (LabJack is not transmitting)
print("waiting on port:", port)

# Loop to keep collecting data
while True:

	try:
		data, addr = a.recvfrom(1024)
		print(data)

		# Add your preferred data collection scheme here

	except KeyboardInterrupt:
		print("UDP receive ended")
		break
