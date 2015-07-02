from highcharts.views import * #SEE WHICH GRAPHS TO IMPORT
import json
import os
from django.conf import settings


class linegraph(HighChartsLineView):
    def get_data(self):
        myfile=os.path.join(settings.BASE_DIR, "preproc/graph.json") #filename
        f = open(myfile, "r")
        data = json.load(f)
        f.close()

        # if title was provided requesting the url, use it as chart
        # title, otherwise hope to find title in json
        if 'title' in self.kwargs:
            data['title'] = {}
            data['title']['text'] = self.kwargs['title']

        how_many_series = len(data['series'])

        if 'end' in self.kwargs:
            end = int(self.kwargs['end'])
            for i in range(how_many_series):
                data['series'][i]['data'] = data['series'][i]['data'][:end]

        if 'begin' in self.kwargs:
            begin = int(self.kwargs['begin'])
            for i in range(how_many_series):
                data['series'][i]['data'] = data['series'][i]['data'][begin:]

        print len(data['series'][0]['data'])
        return data

