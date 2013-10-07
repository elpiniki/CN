##########################################################################
""" MakeUpperCaseServerUsingTCP.py   
                                         
  ELPINIKI APOSTOLAKI-IOSIFIDOU & NICK WAITE                                 
  COMPUTER NETWORKS, FALL 2013                    
  10/03/2013                                         
  This module is the server side of a simple client-server application for socket programming using TCP. The server receives characters (data) from the client, converts these characters to uppercase. Then, the server sends the modified characters back to the client.                
"""

# enable python to create sockets within the program
from socket import *

# provide the port number
serverPort = 12345

# create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))

# server begins listening for incoming TCP requests
serverSocket.listen(100)

print ("The server is ready to receive ... ")
while 1:
    # server waits for incoming requests; new socket created on return
    connectionSocket, addr = serverSocket.accept()
    print addr 
    # read a sentence of bytes from socket sent by the client
    sentence = connectionSocket.recv(1024)
	 
    # convert the sentence to upper case
    capitalizedSentence = sentence.upper()
	 
    # send back modified sentence over the TCP connection
    connectionSocket.send(capitalizedSentence)
	 
    # close the TCP connection; the welcoming socket continues
    connectionSocket.close()

