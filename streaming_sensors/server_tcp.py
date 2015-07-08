#!/usr/bin/python
 
# Import all from module socket
from socket import *
#Importing all from thread
from thread import *
 
# Defining server address and port
host = '0.0.0.0'  #'localhost' or '127.0.0.1' or '' are all same
port = 5200 #Use port > 1024, below it all are reserved
 
#Creating socket object
sock = socket()
#Binding socket to a address. bind() takes tuple of host and port.
sock.bind((host, port))
#Listening at the address
sock.listen(5) #5 denotes the number of clients can queue
 
def clientthread(conn,addr):
#infinite loop so that function do not terminate and thread do not end.
  while True:
#Sending message to connected client
    conn.send('Hi! I am server\nsend me all your data!\n') #send only takes string
#Receiving from client
    data = conn.recv(1024) # 1024 stands for bytes of data to be received
    print 'Message['+str(addr[0])+':'+str(addr[1])+'] - '+data
 
while True:
#Accepting incoming connections
  conn, addr = sock.accept()
  print addr,conn
#Creating new thread. Calling clientthread function for this function and passing conn as argument.
  start_new_thread(clientthread,(conn,addr)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
 
conn.close()
sock.close()