import socket

port_a = 30325
port_b = 30326
port_c = 30327
port_d = 30328
port_e = 30329

a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
a.bind(("", port_a))

b = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
b.bind(("", port_b))

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.bind(("", port_c))

d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
d.bind(("", port_d))

e = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
e.bind(("", port_e))

print("waiting on port:", port_a)
print("waiting on port:", port_b)
print("waiting on port:", port_c)
print("waiting on port:", port_d)
print("waiting on port:", port_e)

while True:

	try:
		data, addr = a.recvfrom(1024)
		print(data)

		# data, addr = b.recvfrom(1024)
		# print(data)
		#
		# data, addr = c.recvfrom(1024)
		# print(data)
		#
		# data, addr = d.recvfrom(1024)
		# print(data)
		#
		# data, addr = e.recvfrom(1024)
		# print(data)

	except KeyboardInterrupt:
		print("UDP receive ended")
		break
