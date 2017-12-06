# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SensorData(models.Model):

	date_stamp = models.DateTimeField('Date')
	temperature = models.DecimalField(default=0,max_digits=10, decimal_places=2)
	orp = models.DecimalField(default=0,max_digits=10, decimal_places=2)
	ph = models.DecimalField(default=0,max_digits=10, decimal_places=2)
	conductivity = models.DecimalField(default=0,max_digits=10, decimal_places=2)
	flow_rate = models.DecimalField(default=0,max_digits=10, decimal_places=2)
	turbidity = models.DecimalField(default=0,max_digits=10, decimal_places=2)