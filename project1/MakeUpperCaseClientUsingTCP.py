##########################################################################
"""  MakeUpperCaseClientUsingTCP.py                                     

  ELPINIKI APOSTOLAKI-IOSIFIDOU & NICK WAITE                                 
  COMPUTER NETWORKS, FALL 2013                    
  10/03/2013                                        
   This module is the client side of a simple client-server application for socket programming using TCP. The client reads the characters typed (lowercase characters) and sends them to the server. Then, the client receives the modified data from the server (uppercase characters) and displays the data on its screen. 
"""

# enable python to create sockets within the program
from socket import *

# provide the IP address of the server
serverName = "10.0.0.132"

# provide the port number
serverPort = 12345

# create TCP socket, called clientSocket, on client to use for connecting to remote server.  
# indicate the server's remote listening port type SOCK_STREAM for TCP
clientSocket = socket(AF_INET, SOCK_STREAM)

# initiate the TCP connection between the client and server
clientSocket.connect((serverName,serverPort))

# interactively get user's line to be converted
sentence = raw_input("Input lowercase sentence: ").encode("utf-8")

# send the user's line over the TCP connection
# No need to specify server name, port
clientSocket.send(bytes(sentence))

# get user's line back from server having been modified by the server
modifiedSentence = clientSocket.recv(1024)

# output the modified user's line 
print ("From Server: ", modifiedSentence)

# close the TCP connection
clientSocket.close()

