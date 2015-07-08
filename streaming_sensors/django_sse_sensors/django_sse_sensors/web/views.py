__author__ = 'marco'

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
import redis

import time


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

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        ps = r.pubsub()
        ps.subscribe('testdata')
        ts = time.time()
        while True:
            acc = 0
            acc2 = 0
            acc3 = 0
            i = 0
            tsnew = ts

            while tsnew <= ts+0.1:
                pac = ps.get_message("testdata")
                if pac:
                    pac = json.loads(pac['data'])
#                    print pac
                    acc = acc + pac['values'][0]
                    acc2 = acc2 + pac['values'][1]
                    acc3 = acc3 + pac['values'][2]
                    i += 1
                    tsnew = time.time()
            self.sse.add_message("message", json.dumps({'timestamp': ts, 'values': [acc/i, acc2/i, acc3/i]}))
            ts = time.time()

#            print acc/i
#            print i
            yield


