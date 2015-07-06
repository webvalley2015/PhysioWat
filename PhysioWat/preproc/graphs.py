from highcharts.views import *  # SEE WHICH GRAPHS TO IMPORT
from jsongen import getavaliabledatavals, makejson
import json


class linegraph(HighChartsLineView):


    def get_data(self):
        #read parameters from url
        urlTmp = self.kwargs
        #get data type list
        vals = getavaliabledatavals(urlTmp['id_num'])
        #vals = vals[1:]
        data = makejson("raw", urlTmp['id_num'], vals)
        data = json.loads(data)
        #print "here"
        #print data
        for i in data['series']:
            #print i['name']
            if (i['name'] == 'timeStamp'):
                times = i['data']

        #print times

        #print "fsahdiasdjasdioadsjdoisj"
        for i in data['series']:
            #print 'i[data]', len(i['data'])
            i['data'] = [ [times[cont], i['data'][cont]  ] for cont in range(len(i['data'])) ]
        #print data['series']
        data['chart'] = {"renderTo":"#temporary-processing"}
        return data
