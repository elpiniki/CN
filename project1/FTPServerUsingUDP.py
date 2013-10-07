##########################################################################
""" FTPServerUsingTCP.py   
																				 
	ELPINIKI APOSTOLAKI-IOSIFIDOU & NICK WAITE                                 
	COMPUTER NETWORKS, FALL 2013                    
	10/03/2013                                         
	This module is the server side of a simple client-server application for socket programming using TCP. As a server, it receives characters (data) from the client, converts these characters to uppercase and sends the modified characters back to the client.                
"""

import socket
from collections import defaultdict
import struct
import os
import random


def counter():
	count = 0
	while True:
		yield count
		count += 1

file_index = defaultdict( counter().next )
file_handle = {}


def broken_send(sock, *args):
	if random.choice((True,False)):
		sock.sendto(*args)
	else:
		print "packet lost"


# STUDENTS: randomize this port number (use same one that client uses!)
serverPort = 12345

# create TCP welcoming socket
sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
sock.bind(('localhost', serverPort))

print ("Server is up:", serverPort)

while True:
		data, requestor = sock.recvfrom(8192)
		protocol, cmd =  data[:2]
		body = data[2:]
		assert protocol == '\x33'					# make sure it's our protocol

		if cmd == "\01":
			reqid, fname = struct.unpack(">H", body[:2])[0], body[2:]
			print requestor, "HEAD", reqid, fname,
			fid = file_index[fname]
			print "-->", fid,
			if fid not in file_handle:
				print "NEW",
				file_handle[fid] = file(fname, "rb")	# open file and put handle in dictionary

			print
			f = file_handle[fid]										# find length & cache file into memory
			f.seek(0, os.SEEK_END)
			fsize = f.tell()
			broken_send(sock, "\x33\x81" + struct.pack(">HII", reqid, fid, fsize ), requestor)

		elif cmd == "\02":
			fid, offset, length = struct.unpack(">IIH", body)
			print requestor, "GET", fid, offset, length
			fhandle = file_handle[fid]
			fhandle.seek(offset)
			rdata = fhandle.read(length)
#			assert len(rdata) == length, str(len(rdata)) + "  " + str(length)

			broken_send(sock, "\x33\x82" + struct.pack(">II", fid, offset) + rdata, requestor)


