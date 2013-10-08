##########################################################################
"""  FTPClientUsingUDP.py                                     

	ELPINIKI APOSTOLAKI-IOSIFIDOU & NICK WAITE                                 
	COMPUTER NETWORKS, FALL 2013                    
	10/03/2013                                        
	UDP file transfer client. 
	Connects to <ServerIP>, downloads <RemoteFileName> and saves it to file called <LocalFileName>.
	Uses only UDP packets, but is reliable. 

	Usage:
	FTPClientUsingUDP.py <ServerIP> <RemoteFileName> <LocalFileName>
"""

import socket
import sys
import random
import struct

server = (sys.argv[1], 12345)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.5)


def get_file(sock, server, fname):
	recvbuf = ""

	while True: # get file INFO
		try:
			outreqid = random.randint(0, 65535)										# create random 16-bit request ID 
			print "INFO (seq# %d) '%s' -->" % (outreqid, fname),
			sock.sendto("\x33\x01" + struct.pack(">H", outreqid ) + fname, server )	# ask serve: INFO? <RequestID> <filename>
			data, sender = sock.recvfrom(8192)										# get response
			assert sender == server, str(sender) + " is not " + str(server)			# ensure rx'd packet is from server
 
			header, inreqid, fid, fsize = struct.unpack(">2sHII", data )			# response: INFO <RequestID> <FileID> <FileSize>
			assert header == "\x33\x81" and inreqid == outreqid						# ensure packet correct
			print "#%d  %d bytes" % (fid, fsize)
			break																	# go along
		except (socket.timeout, AssertionError) as poo:									# if timeout or bad packet, re-request
			print poo
			pass

	length = 1024																	# max data chunk size to request

	while len(recvbuf) < fsize:														# get data until the data's all got

		while True: # get file DATA
			try:
				print "GET #%d (%s): %dB from %d -->" % ( fid, fname, length, len(recvbuf)),
				sock.sendto("\x33\x02" + struct.pack(">IIH", fid, len(recvbuf), length ), server )
																					# ask server: GET <FileID> <FileOffset> <DataLength>
				data, sender = sock.recvfrom(8192)									# get response
				assert sender == server, str(sender) + " is not " + str(server)		# ensure response is from server
				header, infid, inoffset = struct.unpack(">2sII", data[:10] )		# response: GOT <FileID> <FileOffset> <data>
				rxbytes = data[10:]
				print len(rxbytes), 'bytes'
				assert header == "\x33\x82" and infid == fid and inoffset == len(recvbuf)	# verify response is expected one
#				assert len(rxbytes) == length
				recvbuf += rxbytes													# add response to end of buffer
				break

			except (socket.timeout, AssertionError) as poo:								# bad packet or lost packet
				print poo
				pass
	return recvbuf																	# file all gotten, return it


recvdfile = get_file(sock, server, sys.argv[2])
#print recvdfile
file(sys.argv[3], 'wb').write(recvdfile)

sock.close()
