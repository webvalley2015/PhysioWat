from highcharts.views import *  # SEE WHICH GRAPHS TO IMPORT
from jsongen import getavaliabledatavals, makejson
import json
from PhysioWat.models import SensorRawData, Preprocessed_Data
from operator import itemgetter

class linegraph(HighChartsLineView):


    def get_data(self):
        #read parameters from url
        urlTmp = self.kwargs
        #get data type list
        vals = getavaliabledatavals(urlTmp['id_num'])
        data = makejson(urlTmp['elab'], urlTmp['id_num'], vals)
        data = json.loads(data)
        for i in data['series']:
            if (i['name'] == 'timeStamp'):
                times = i['data']

        for i in data['series']:
            i['data'] = [ [times[cont], i['data'][cont]  ] for cont in range(len(i['data'])) ]
        data['chart'] = {"renderTo":"#temporary-processing"}
        return data


class linegraph2(HighChartsMultiAxesView):
    legend = {'enabled': True, 'layout': 'vertical', 'align': 'right',
                'verticalAlign': 'top', 'x': 10, 'y': 100, 'borderWidth': 0, }

    def get_data(self):
        #read parameters from url
        urlTmp = self.kwargs
        #get data type list
        # vals = getavaliabledatavals(urlTmp['id_num'])
        if urlTmp['elab'] == "raw":
            data = SensorRawData.objects.filter(recording_id=urlTmp['id_num']).order_by('id')
            self.title = 'Raw Data'
        elif urlTmp['elab'] == "proc":
            data = Preprocessed_Data.objects.filter(recording_id=urlTmp['id_num']).order_by('id')
            self.title = 'Preprocessed Data'


        self.yaxis = {'title': {'text': ''}, 'min': 0}
        data_tmp = [i.store for i in data]
        self.series = []
        tmp = {k: (map(float,map(itemgetter(k), data_tmp))) for k in data_tmp[0]}

        for k in tmp.keys():
            tmplist = [[tmp['TIME'][i], tmp[k][i]] for i in xrange(len(tmp[k]))]
            self.series.append({'data': tmplist, 'name': k})

        #vals = vals[1:]
        # data = makejson(urlTmp['elab'], urlTmp['id_num'], vals)
        # data = json.loads(data)
        #print "here"
        #print data
        # for i in data['series']:
        #     #print i['name']
        #     if (i['name'] == 'timeStamp'):
        #         times = i['data']

        #print times

        #print "fsahdiasdjasdioadsjdoisj"
        # for i in data['series']:
        #     #print 'i[data]', len(i['data'])
        #     i['data'] = [ [times[cont], i['data'][cont]  ] for cont in range(len(i['data'])) ]
        # #print data['series']
        data = super(linegraph2, self).get_data()
        data['chart'] = {"renderTo":"#temporary-processing"}
        return data
