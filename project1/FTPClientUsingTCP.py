##########################################################################
"""  FTPClientUsingTCP.py                                     

  ELPINIKI APOSTOLAKI-IOSIFIDOU & NICK WAITE                                 
  COMPUTER NETWORKS, FALL 2013                    
  10/03/2013                                        
   This module is the client side of a simple client-server application for socket programming using TCP. As a client, it asks from the user to type lowercase characters, reads these characters from its keyboard and sends them to the server. Then, the client receives the modified data and displays the line on its screen. 
"""

from socket import *
import sys

# STUDENTS - replace your server machine's name or IP address
serverName = "127.0.0.1"
serverPort = 12345
clientSocket = socket(AF_INET, SOCK_STREAM)

# open the TCP connection
clientSocket.connect((serverName,serverPort))

def get_file(clientSocket, test):
    cmd = 'get\n%s\n' % (test)
    clientSocket.sendall(cmd)
    r = clientSocket.recv(2)
    assert r == "ok"

    size = int(clientSocket.recv(16))
    recvd = ''
    while size > len(recvd):
        data = clientSocket.recv(1024)
        if not data: 
            break
        recvd += data
    clientSocket.sendall('ok')
    return recvd

recvdfile = get_file(clientSocket, sys.argv[1])
file(sys.argv[1], 'wb').write(recvdfile)

clientSocket.sendall('end\n') 
clientSocket.close()
