import socket
import random
import sys
import time


#!usr/bin/python
from socket import *
 
#host = 'localhost' # '127.0.0.1' can also be used
#port = 52000
 
host = '192.168.205.160' # '127.0.0.1' can also be used
port = 8002


SEED = 12335+int(sys.argv[1])
NAME=sys.argv[2]
sock = socket()
#Connecting to socket
sock.connect((host, port)) #Connect takes tuple of host and port
#data = sock.recv(1024)
#print data
 
random.seed(SEED)
#dt=random.random()
#dt=0.1
#Infinite loop to keep client running.
while True:
	rn=random.random()
	message=NAME+": "+str(rn)+'\n'
	sock.send(message)
	dt=random.random()
	time.sleep(1*dt)
 
sock.close()

