##########################################################################
""" MakeUpperCaseServerUsingUDP.py                                     
 
ELPINIKI APOSTOLAKI-IOSIFIDOU & NICK WAITE                                 
  COMPUTER NETWORKS, FALL 2013                    
  10/03/2013                                         
	This module is the server side of a simple client-server application for socket programming using UDP. The server receives characters (data) from the client, converts these characters to uppercase. Then, the server sends the modified characters back to the client.             
"""

# enable python to create sockets within the program
from socket import *

# provide the port number
serverPort = 12345

# create UDP socket and bind to your specified port
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

print ("The server is ready to receive ... ")
while 1:
    # read client's message and remember client's address (IP and port)
    message, clientAddress = serverSocket.recvfrom(2048)
	
    # change client's sentence to upper case letters
    modifiedMessage = message.upper()
	
    # send back modified sentence to the client using remembered address
    serverSocket.sendto(modifiedMessage, clientAddress)

