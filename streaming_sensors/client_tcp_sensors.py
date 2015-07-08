import socket
import random
import sys
import time

import struct
import time

from socket import *


def recv_int(f):
	x=struct.unpack('!i', f.recv(4))[0]
#	print 'int: ', x
	return x

def recv_long(f):
	x=struct.unpack('!q', f.recv(8))[0]
#	print 'long: ', x
	return x

def recv_byte(f):
	x=ord(f.recv(1)[0])
#	print 'byte: ', x
	return x

def recv_string(f):
	l = ord(f.recv(1)[0])
	x=f.recv(l)
#	print 'str: ', x
	return x

def recv_double(f):
	x=struct.unpack('!d', f.recv(8))[0]
#	print 'long: ', x
	return x


def recv_header(f):
	header={}
	recv_byte(f)
	recv_byte(f)
	recv_byte(f)
	ns=recv_byte(f)
	header['sessionTag']=recv_string(f)
	header['sensors']=[]
	for i in xrange(ns):
		recv_byte(f)
		recv_byte(f)
		recv_byte(f)	
		snrs={}
		snrs['type']=recv_string(f)
		snrs['name']=recv_string(f)
		nl=recv_byte(f)
		snrs['cols']=[]
		for l in xrange(nl):
			snrs['cols'].append(recv_string(f))
		header['sensors'].append(snrs)
	return header

def recv_pack(f,header):
	recv_byte(f)
	t = recv_byte(f)
	data={}
	if(t==100):
		ids=recv_byte(f)
		data['type']=ids
		data['timestamp']=recv_long(f)
		data['values']=[]
		for i in xrange(len(header['sensors'][ids]['cols'])):
			data['values'].append(recv_double(f))
	elif(t==101):
		data['type']='event'
		data['timestamp']=recv_long(f)
		ids=recv_byte(f)
		data['code']=recv_int(f)
		data['message']=recv_string(f)

	return data


def main():
	host = '192.168.205.243' # '127.0.0.1' can also be used
	port = 2000
	 
	sock = socket()
	#Connecting to socket
	sock.connect((host, port)) #Connect takes tuple of host and port

	#header=recv_header(sock)
	#print header


	header=recv_header(sock)
	print header
	while True:
		print recv_pack(sock,header)
	 
	sock.close()	

if __name__ == "__main__":
	main()


