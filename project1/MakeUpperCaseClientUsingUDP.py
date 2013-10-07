##########################################################################
"""  MakeUpperCaseClientUsingUDP.py                                      
  
ELPINIKI APOSTOLAKI-IOSIFIDOU & NICK WAITE                                 
  COMPUTER NETWORKS, FALL 2013                    
  10/03/2013                                        
     This module is the client side of a simple client-server application for socket programming using UDP. The client reads the characters typed (lowercase characters) and sends them to the server. Then, the client receives the modified data from the server (uppercase characters) and displays the data on its screen.                
"""

# enable python to create sockets within the program
from socket import *

# provide the IP address of the server
serverName = "10.0.0.132"
   
# provide the port number
serverPort = 12345

# create UDP socket, called clientSocket. 
# indicate the server's remote listening port type SOCK_DGRAM for UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)

# interactively get user's line to be converted
message = raw_input("Input lowercase sentence: ").encode("utf-8")

# send user's sentence out socket; destination host and port number req'd
clientSocket.sendto(bytes(message), (serverName, serverPort))

# receive modified sentence in all upper case letters from server
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# output modified sentence and close the socket
print (modifiedMessage)
clientSocket.close()

