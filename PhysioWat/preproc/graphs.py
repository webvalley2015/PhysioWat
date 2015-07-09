from highcharts.views import *  # SEE WHICH GRAPHS TO IMPORT
from jsongen import getavaliabledatavals, makejson
import json
from PhysioWat.models import SensorRawData, Preprocessed_Data, Preprocessed_Recording
from operator import itemgetter


class linegraph(HighChartsLineView):
    def get_data(self):
        # read parameters from url
        urlTmp = self.kwargs
        # get data type list
        vals = getavaliabledatavals(urlTmp['id_num'])
        data = makejson(urlTmp['elab'], urlTmp['id_num'], vals)
        data = json.loads(data)

        timestamplist = ['time', 'TIME', 'Time', 'TimeStamp', 'timeStamp', 'timestamp', 'Timestamp']
        for i in data['series']:
            if (i['name'] in timestamplist):
                times = i['data']

        for i in data['series']:
            i['data'] = [[times[cont], i['data'][cont]] for cont in range(len(i['data']))]
        data['chart'] = {"renderTo": "#temporary-processing"}
        return data


class linegraph2(HighChartsMultiAxesView):
    legend = {'enabled': True, 'layout': 'vertical', 'align': 'right',
              'verticalAlign': 'top', 'x': 10, 'y': 100, 'borderWidth': 0, }

    def get_data(self, data=None):
        # read parameters from url
        urlTmp = self.kwargs
        # get data type list
        # vals = getavaliabledatavals(urlTmp['id_num'])
        data = []
        if urlTmp['elab'] == "raw":
            idx = [(0, 'raw')]
            data.append(SensorRawData.objects.filter(recording_id=urlTmp['id_num']).order_by('id'))
            self.title = 'Raw Data'
        elif urlTmp['elab'] == "proc":
            idx = Preprocessed_Recording.objects.filter(batch_id=urlTmp['id_num']).values_list("pk", "signal_type_name")
            for i in idx:
                data.append(Preprocessed_Data.objects.filter(pp_recording_id=i[0]).order_by('id'))
            self.title = 'Preprocessed Data'

        print "DEBUG data", data
        print "DEBUG data", data, len(data), type(data)

        self.yaxis = {'title': {'text': ''}}

        data_tmp = []
        for d in data:
            data_tmp.append([i.store for i in d])

        self.series = []

        for j, d in enumerate(data_tmp):
            tmp = {k: (map(float, map(itemgetter(k), d))) for k in d[0]}


            # CALCULATING SAMPLING FREQ.
            samling_freq = 0.0
            for i in range(0, 10):
                samling_freq = samling_freq + (tmp['TIME'][i + 1] - tmp['TIME'][i])
            samling_freq = samling_freq / 10
            samling_freq = int(round(1 / samling_freq))
            samling_freq = "%d" % samling_freq
            samling_freq = str(' sampling frequency: ' + str(samling_freq) + 'Hz')
            self.subtitle = samling_freq

            # ADDING TIMESTAMP
            for k in tmp.keys():
                tmplist = [[tmp['TIME'][i] * 1000, tmp[k][i]] for i in xrange(len(tmp[k]))]
                self.series.append({'data': tmplist, 'name': '{}_{}'.format(k, str(idx[j][1]))})
        # print times

        # print "fsahdiasdjasdioadsjdoisj"
        # for i in data['series']:
        #     #print 'i[data]', len(i['data'])
        #     i['data'] = [ [times[cont], i['data'][cont]  ] for cont in range(len(i['data'])) ]
        # #print data['series']
        data = super(linegraph2, self).get_data()
        # print data

        data['chart'] = {"renderTo": "#temporary-processing"}
        return data

class linegraph3(HighChartsMultiAxesView):
    legend = {'enabled': True, 'layout': 'vertical', 'align': 'right',
              'verticalAlign': 'top', 'x': 10, 'y': 100, 'borderWidth': 0, }

    def get_data(self, data, xcategories=None, title=None):
        data_tmp = []
        print xcategories
        for i in data:
            data_tmp.append(i[1])
        self.yaxis = {'title': {'text': ''}}
        self.series = [{'name':'Precision', 'data':data_tmp, 'type':'scatter'}]
        #self.series.append({})
        self.categories = xcategories
        # print data
        self.title=title

        data = super(linegraph3, self).get_data()
        return data

def somma(matrix):
    total = 0
    for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                total += matrix[i][j]

    return total

class heatmap(HighChartsHeatMapView):
    legend = {'enabled': True, 'layout': 'vertical', 'align': 'right',
              'verticalAlign': 'top', 'x': 10, 'y': 100, 'borderWidth': 0, }

    def get_data(self, matrix):
        seriesTemp=[]
        # the confusion matrix is returned as a list of list of dimension n*n, where n is the number of labels
        # reformatting confusion matrix


        n_labels = len(matrix[0])
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                value =  float(matrix[i][j]) / somma(matrix) * 100.0
                value = float("%.2f" % value)
                seriesTemp.append([j, len(matrix)-i-1, value] )

        #print seriesTemp
        self.title = "Results - confusion matrix"
        self.subtitle = "the value in the cells is the percentage of combinations predicted label - real label"
        self.xaxis = {'categories':range(n_labels)}
        self.yaxis = {'categories':range(n_labels)}
        seriesTemp = {'name' : 'conf-mat', 'data': seriesTemp,  'dataLabels': {'enabled': True, 'color': '#000000'} }
        self.series = [seriesTemp]
        self.coloraxis = {'minColor': '#FFFFFF',
                          'maxColor': '#00A0FF',}

        data = super(heatmap, self).get_data()
        return data
