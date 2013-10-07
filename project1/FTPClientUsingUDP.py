##########################################################################
"""  FTPClientUsingTCP.py                                     

	ELPINIKI APOSTOLAKI-IOSIFIDOU & NICK WAITE                                 
	COMPUTER NETWORKS, FALL 2013                    
	10/03/2013                                        
	 This module is the client side of a simple client-server application for socket programming using TCP. As a client, it asks from the user to type lowercase characters, reads these characters from its keyboard and sends them to the server. Then, the client receives the modified data and displays the line on its screen. 
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

	while True: # get file info
		try:
			outreqid = random.randint(0, 65535)
			print "INFO (seq# %d) '%s' -->" % (outreqid, fname),
			sock.sendto("\x33\x01" + struct.pack(">H", outreqid ) +fname, server )
			data, sender = sock.recvfrom(8192)
			assert sender == server, str(sender) + " is not " + str(server)
 
			header, inreqid, fid, fsize = struct.unpack(">2sHII", data )
			assert header == "\x33\x81" and inreqid == outreqid
			print "#%d  %d bytes" % (fid, fsize)
			break
		except socket.timeout:
			print "timeout!"
			pass

	length = 1024

	while len(recvbuf) < fsize:
#		getbytes = min(fsize - len(recvbuf), 1024)

		while True: # get file info
			try:
				print "GET #%d (%s): %dB from %d -->" % ( fid, fname, length, len(recvbuf)),
				sock.sendto("\x33\x02" + struct.pack(">IIH", fid, len(recvbuf), length ), server )
				data, sender = sock.recvfrom(8192)
				assert sender == server, str(sender) + " is not " + str(server)
				header, infid, inoffset = struct.unpack(">2sII", data[:10] )
				rxbytes = data[10:]
				print len(rxbytes), 'bytes'
				assert header == "\x33\x82" and infid == fid and inoffset == len(recvbuf)
#				assert len(rxbytes) == length
				recvbuf += rxbytes
				break

			except socket.timeout:
				print "timeout!"
				pass
	return recvbuf


recvdfile = get_file(sock, server, sys.argv[2])
#print recvdfile
file(sys.argv[3], 'wb').write(recvdfile)

sock.close()
