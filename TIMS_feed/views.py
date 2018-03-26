# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
import urllib2
import xmltodict
import json


def get_disruptions(request):
	context = {}
	disruption_data=[]
	template = 'TIMS_feed/map.html'
	if len(disruption_data)==0:
		XML_file = urllib2.urlopen('https://data.tfl.gov.uk/tfl/syndication/feeds/tims_feed.xml?app_id=&app_key=')
		data = XML_file.read()
		XML_file.close()

		data = xmltodict.parse(data)
		for d in data['Root']['Disruptions']['Disruption']:
			lat_lon=d['CauseArea']['DisplayPoint']['Point']['coordinatesLL'].split(',')
			location=' '+d['location'].replace("'","")
			disruption_id='disruption id '+d['@id']
			print 'Disruption id is {0}'.format(disruption_id)
			print 'Location is {0}'.format(location)
			print 'Coordinates are {0}'.format(lat_lon)
			disruption_data.append([float(lat_lon[0]),float(lat_lon[1]),disruption_id+location])
	disruption_data=json.dumps(disruption_data)
	context['disruption_data']=disruption_data
	return render(request,template,context)
