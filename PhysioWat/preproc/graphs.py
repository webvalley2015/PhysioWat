from highcharts.views import *  # SEE WHICH GRAPHS TO IMPORT
from jsongen import getavaliabledatavals, makejson
import json

class linegraph(HighChartsLineView):
    def get_data(self):
        vals = getavaliabledatavals(5)
        vals = vals[1:]
        data = makejson("raw", 5, vals)
        data = json.loads(data)

        data['chart'] = {"renderTo":"#temporary-processing"}
        return data
