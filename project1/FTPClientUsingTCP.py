##########################################################################
"""  FTPClientUsingTCP.py                                     

  ELPINIKI APOSTOLAKI-IOSIFIDOU & NICK WAITE                                 
  COMPUTER NETWORKS, FALL 2013                    
  10/03/2013 
  python version 2.7                                       
   This module is the client side of a client-server application for socket programming using TCP. The client provides the IP of the server and the name of file that he wants to download from the server. The requested file is located at the server. The file is transfered via a TCP connection from the server to the client.  
"""

# enable python to create sockets within the program
from socket import *

# access to some variables, here argv with which command line arguments passed to a Python script
import sys

# enable python to use os for the exception part in case of connection fail
import os

# the IP is given by the user as an argument in the command line
serverName = sys.argv[1]

# provide the port number
serverPort = 12345

# create TCP socket, called clientSocket, on client to use for connecting to remote server.  
# indicate the server's remote listening port type SOCK_STREAM for TCP
clientSocket = socket(AF_INET, SOCK_STREAM)

# initiate the TCP connection between the client and server
try:
    clientSocket.connect((serverName,serverPort))

# exception in case the connection fails
except error as msg:
    print "Unable to open TCP connection"
    print msg
    os.exit()

# function to get remote file, takes in socket and filename, returns string containing bytes of file
def get_file(clientSocket, filename):
    cmd = 'get\n%s\n' % (filename) # built get command
    clientSocket.sendall(cmd) #send command
    r = clientSocket.recv(2)
    assert r == "ok"

    # get the file
    size = int(clientSocket.recv(16))
    recvd = ''
    while size > len(recvd):
        data = clientSocket.recv(1024)
        if not data: 
            break
        recvd += data
    clientSocket.sendall('ok')
    return recvd

recvdfile = get_file(clientSocket, sys.argv[2])
file(sys.argv[2], 'wb').write(recvdfile)

# close TCP connection when the file is sent
clientSocket.sendall('end\n') 
clientSocket.close()
