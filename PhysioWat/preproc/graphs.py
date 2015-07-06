from highcharts.views import *  # SEE WHICH GRAPHS TO IMPORT
from jsongen import getavaliabledatavals, makejson
import json

class linegraph(HighChartsLineView):
    def get_data(self):
        urlTmp = self.kwargs
        vals = getavaliabledatavals(urlTmp['id_num'])
        vals = vals[1:]
        data = makejson("raw", urlTmp['id_num'], vals)
        data = json.loads(data)

        data['chart'] = {"renderTo":"#temporary-processing"}
        return data
