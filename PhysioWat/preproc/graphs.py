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
		#data = super()
		return data


