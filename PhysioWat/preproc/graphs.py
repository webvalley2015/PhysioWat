from highcharts.views import * #SEE WHICH GRAPHS TO IMPORT
import json
import os
from django.conf import settings

class linegraph(HighChartsLineView):
	
	
	def get_data(self, title=""):
		myfile=os.path.join(settings.BASE_DIR, "preproc/graph.json") #filename
		f = open(myfile, "r")
		data = json.load(f)
		f.close()
		# if title was provided requesting the url, use it as chart
		# title, otherwise hope to find title in json
		if title:
			data['title'] = {}
			data['title']['text'] = title
		
		return data
