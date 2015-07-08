import socket
import random
import sys
import time

import struct
import time

from socket import *
from thread import *
import redis
import json

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

def recv_user_pwd(f):
#	recv_byte(f)
	user = recv_string(f)
#	recv_byte(f)
	pwd = recv_string(f)
	return 	user, pwd

def recv_header(f):
	header={}
	recv_byte(f)
	recv_byte(f)
	recv_byte(f)
	ns=recv_byte(f)
	header["sessionTag"]=recv_string(f)
	header["sensors"]=[]
	for i in xrange(ns):
		recv_byte(f)
		recv_byte(f)
		recv_byte(f)	
		snrs={}
		snrs["type"]=recv_string(f)
		snrs["name"]=recv_string(f)
		nl=recv_byte(f)
		snrs["cols"]=[]
		for l in xrange(nl):
			snrs["cols"].append(recv_string(f))
		header["sensors"].append(snrs)
	return header

def recv_pack(f,header):
	recv_byte(f)
	t = recv_byte(f)
	data={}
	if(t==100):
		ids=recv_byte(f)
		data["type"]=ids
		data["timestamp"]=recv_long(f)
		data["values"]=[]
		for i in xrange(len(header["sensors"][ids]["cols"])):
			data["values"].append(recv_double(f))
	elif(t==101):
		data["type"]="event"
		data["timestamp"]=recv_long(f)
		ids=recv_byte(f)
		data["code"]=recv_int(f)
		data["message"]=recv_string(f)

	return data

def clientthread(conn,addr,index_port):
	# you'll first need to open a connection to redis-server
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	p = r.pubsub()
	p.subscribe('testdata')

	# infinite loop so that function do not terminate and thread do not end.
	while True:
		user, pwd = recv_user_pwd(conn)
		if (user != 'User' and pwd != 'password'):
			print user, pwd
			conn.close()
		else:
			header = recv_header(conn)
			print header
			while True:
				rec_pack = recv_pack(conn, header)
				r.publish("testdata", json.dumps(rec_pack)) 
				print rec_pack


def main():
	host = '0.0.0.0' # '127.0.0.1' can also be used
	port = 2000
	 
	sock = socket()
	sock.bind((host, port))
	sock.listen(5)
	#Connecting to socket
#	sock.connect((host, port)) #Connect takes tuple of host and port
	i=1
	while True:
		conn, addr = sock.accept()
		start_new_thread(clientthread,(conn,addr,i))
		i+=1
	#header=recv_header(sock)
	#print header
	 
	conn.close()
	sock.close()	

if __name__ == "__main__":
	main()


