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


# Generator function. Creates an iterator that returns increasing numbers every time it's called
def counter():
	count = 0
	while True:
		yield count
		count += 1

file_index = defaultdict( counter().next )	# maps filenames to numbers
file_handle = {} # maps file id numbers to open file handles


# tests connection reliability by only sometimes actually sending a packet
def broken_send(sock, *args):
	if random.choice((True,False)):
		sock.sendto(*args)
	else:
		print "packet lost"


serverPort = 12345

sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
sock.bind(('localhost', serverPort))					# open UDP socket on server

print ("Server is up:", serverPort)

while True:
		data, requestor = sock.recvfrom(8192)			# get a packet
		protocol, cmd =  data[:2]						# separate header from body
		body = data[2:]
		assert protocol == '\x33'						# make sure it's our protocol

		if cmd == "\01":								# file INFO command
			reqid = struct.unpack(">H", body[:2])[0]	# first 2 bytes of body are request number
			fname = body[2:]							# rest of body is desired filename
			print requestor, "HEAD", reqid, fname,		# print packet info
			fid = file_index[fname]						# look up filename
			print "-->", fid,
			if fid not in file_handle:					# if file's not open
				print "NEW",
				file_handle[fid] = file(fname, "rb")	# open file and put handle in dictionary
														# note: this leaves file open indefinitely.
														# in a real server we would use some kind of LRU
														# caching scheme to close files if left inactive

			print
			f = file_handle[fid]						# find length & cache file into memory
			f.seek(0, os.SEEK_END)
			fsize = f.tell()
			response = "\x33\x81" + struct.pack(">HII", reqid, fid, fsize ) # assemble info packet
			broken_send(sock, response, requestor)		# send response
														
		elif cmd == "\02":								# file GET command
			fid, offset, length = struct.unpack(">IIH", body) # GET <fileID> <byte_offset> <n_bytes>
			print requestor, "GET", fid, offset, length
			fhandle = file_handle[fid]					# get file handle for this ID
			fhandle.seek(offset)						
			rdata = fhandle.read(length)				# read the desired bytes from the file
			response = "\x33\x82" + struct.pack(">II", fid, offset) + rdata # response: <fileID> <byte_offset> <data>
			broken_send(sock, response, requestor)


