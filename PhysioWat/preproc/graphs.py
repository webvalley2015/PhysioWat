from highcharts.views import * #SEE WHICH GRAPHS TO IMPORT
import json
import os
from django.conf import settings


class linegraph(HighChartsLineView):
    def get_data(self, begin=-1, end=-1):
        myfile=os.path.join(settings.BASE_DIR, "preproc/graph.json") #filename
        f = open(myfile, "r")
        data = json.load(f)
        f.close()


        # if title was provided requesting the url, use it as chart
        # title, otherwise hope to find title in json
        if 'title' in self.kwargs:
            data['title'] = {}
            data['title']['text'] = self.kwargs['title']

        print "EHY, LOOK AT ME!!!!"
        print type(data)

        how_many_series = len(data['series'])

        print "how", how_many_series
        if begin != -1:
            for i in range(how_many_series):
                data['series'][i]['data'] = [begin:]

        if end != -1:
            for i in range(how_many_series):
                data['series'][i]['data'] = [:end]

        return data

