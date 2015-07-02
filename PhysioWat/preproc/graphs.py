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
			
		print "EHY, LOOK AT ME!!!!"
		print type(data)	
		
		how_many_series = len(data['series'])
		
		print "how", how_many_series
		for i in range(len(data['series'])):
			print len(data['series'][i]['data'])

		if 'begin' in self.kwargs:
			begin = int(self.kwargs['begin'])
			for i in range(how_many_series):
				data['series'][i]['data'] = data['series'][i]['data'][begin:]
		
		if 'end' in self.kwargs:
			end = int(self.kwargs['end'])
			for i in range(how_many_series):
				data['series'][i]['data'] = data['series'][i]['data'][:end]
	

		for i in range(len(data['series'])):
			print len(data['series'][i]['data'])


		return data

