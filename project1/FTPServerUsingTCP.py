##########################################################################
""" FTPServerUsingTCP.py   
																				 
	ELPINIKI APOSTOLAKI-IOSIFIDOU & NICK WAITE                                 
	COMPUTER NETWORKS, FALL 2013                    
	10/03/2013                                         
	This module is the server side of a simple client-server application for socket programming using TCP. As a server, it receives characters (data) from the client, converts these characters to uppercase and sends the modified characters back to the client.                
"""

from socket import *

# STUDENTS: randomize this port number (use same one that client uses!)
serverPort = 12345

# create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort)) #serverSocket = c

# server begins listening for incoming TCP requests
serverSocket.listen(100)
#s,a = serverSocket.accept()

print ("The server is ready to send ... ")
while 1:
		# server waits for incoming requests; new socket created on return
		connectionSocket, addr = serverSocket.accept()
		print addr 
		data = connectionSocket.recv(1024)
		pkt = data.split("\n")
		cmd = pkt[0]
#    cmd = data[:data.find('\n')]
		
		if cmd =='get':
			x, file_name, x = data.split('\n', 2)
			connectionSocket.sendall('ok')
	
			data = file(file_name, 'rb').read()
			connectionSocket.sendall('%16d' % len(data))
			connectionSocket.sendall(data)
			connectionSocket.recv(2)
		#capitalizedSentence = sentence.upper()
	 
		# send back modified sentence over the TCP connection
		#connectionSocket.send(capitalizedSentence)
	 
		# close the TCP connection; the welcoming socket continues
		if cmd == 'end':
			connectionSocket.close()
			break

