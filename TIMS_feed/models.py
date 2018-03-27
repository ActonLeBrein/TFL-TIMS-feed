# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Disruptions(models.Model):
	id=models.IntegerField(primary_key=True)
	street_name=models.CharField(max_length=200)
	longitude=models.FloatField(null=False)
	latitude=models.FloatField(null=False)