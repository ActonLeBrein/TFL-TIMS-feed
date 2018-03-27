# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
from TIMS_feed.models import Disruptions
import urllib2
import xmltodict
import json

def get_disruptions(request):
	context = {}
	disruption_data=[]
	template = 'TIMS_feed/map.html'
	XML_file = urllib2.urlopen('https://data.tfl.gov.uk/tfl/syndication/feeds/tims_feed.xml?app_id=&app_key=')
	data = XML_file.read()
	XML_file.close()
	data = xmltodict.parse(data)

	for d in data['Root']['Disruptions']['Disruption']:
		id=int(d['@id'])
		lat_lon=d['CauseArea']['DisplayPoint']['Point']['coordinatesLL'].split(',')
		location=d['location'].replace("'","")
		res=Disruptions.objects.filter(id=id)
		if len(res)==0:
			disruption_data.append([float(lat_lon[0]),float(lat_lon[1]),'disruption id '+str(id)+' '+location])
			dis=Disruptions.objects.create(id=id,street_name=location,longitude=float(lat_lon[0]),latitude=float(lat_lon[1]))
		else:
			res=res[0]
			disruption_data.append([res.longitude,res.latitude,'disruption id '+str(res.id)+' '+res.street_name])

	disruption_data=json.dumps(disruption_data)
	context['disruption_data']=disruption_data
	return render(request,template,context)
