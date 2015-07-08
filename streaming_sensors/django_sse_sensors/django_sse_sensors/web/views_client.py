# Create your views here.

from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.utils.timezone import now

from django_sse.views import BaseSseView
import json

import struct
import time
import random
from socket import *

import time



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


class Home1(View):
    def get(self, request):
        return render_to_response('home3.html', {},
                                  context_instance=RequestContext(request))


class Home2(View):
    def get(self, request):
        return render_to_response('home2.html', {},
                                  context_instance=RequestContext(request))


class MySseEvents(BaseSseView):
    def iterator(self):

        host = '192.168.210.161' # '127.0.0.1' can also be used
        port = 2000

        sock = socket()
        #Connecting to socket
        sock.connect((host, port))

        header = recv_header(sock)
        #print header
        ts = time.time()
        while True:
            acc = 0
            acc2 = 0
            acc3 = 0
            i = 0
            tsnew = ts

            while tsnew <= ts+0.1:
                pac = recv_pack(sock, header)
                acc = acc + pac['values'][0]
                acc2 = acc2 + pac['values'][1]
                acc3 = acc3 + pac['values'][2]
                i += 1
                tsnew = time.time()
            #print recv_pack(sock, header)
            #self.sse.add_message("message", json.dumps({'values': [0.22 + random.uniform(0.1, 0.9)], 'timestamp': int(time.time())}))
            self.sse.add_message("message", json.dumps({'timestamp': ts, 'values': [acc/i, acc2/i, acc3/i]}))
            ts = time.time()

#            print acc/i
#            print i
            yield
        # sock.close()


