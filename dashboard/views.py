# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views import generic
from .models import SensorData
from django.http import JsonResponse
from django.core.mail import send_mail
from datetime import datetime
from pytz import timezone

import json
import threading
import pytz
import serial
import time
import random

recipient_email = 'u12004767@tuks.co.za'
sender_email = 'stefancknoll@gmail.com'
time_zone = pytz.timezone('Africa/Johannesburg')

serial_object = serial.Serial()
serial_object.port = '/dev/ttyUSB0'
serial_object.baudrate = 9800
serial_object.timeout = 1

error_count = 0
is_server_connected = False
is_client_connected = False

system_fault = False

def home(request):
	
	return render(request, 'dashboard/index.html')

class HistoryListView(generic.ListView):

	template_name = 'dashboard/history.html'
	model = SensorData

def systemtest(request):
	
	return render(request, 'dashboard/systemtest.html')

def close_flow_water(request):

	print 'Close_flow_command received'
	send_Data(b'c');
	json_obj = {'isClosed':True}
	return JsonResponse(json_obj)

def open_flow_water(request):

	print 'Open_flow_command received'
	send_Data(b'o');
	json_obj = {'isClosed':False}
	return JsonResponse(json_obj)

def send_testemail(request):

	print 'Send_testemail_command received'
	send_email(False,'')
	json_obj = {'mail_sent':True}
	return JsonResponse(json_obj)
		
def send_Data(message):

	global is_server_connected
	global is_client_connected
	global error_count

	try:

		if (serial_object.is_open == False):
			serial_object.open()

	except Exception as e:
	
		print 'Connect ZigBee module!'
		is_server_connected = False

	if (serial_object.is_open == True):

		is_server_connected = True
		serial_object.reset_input_buffer()
		serial_object.reset_output_buffer()
		serial_object.write(message)
		time.sleep(0.05)
		received_data = serial_object.readline()
		serial_object.close()
		print 'data',received_data

		try:

			json.loads(received_data)


		except ValueError:

			print 'JSON Not Valid!'
			error_count += 1

			if (error_count == 5):
				is_client_connected = False
				error_count = 0

		else:

			print 'JSON Valid!'
			is_client_connected = True
			error_count = 0

			#create json and insert received data
			return json.loads(received_data)

	return False

def auto_data_save():

	global time_zone

	threading.Timer(30, auto_data_save).start()

	print 'Auto Saving Progress...'

	json_obj = send_Data(b'r');

	if (json_obj):

		while (len(SensorData.objects.all()) > 100):
			SensorData.objects.all()[0].delete()

		data_entry = SensorData()
		data_entry.date_stamp = datetime.now(time_zone)
		data_entry.ph = json_obj['S1']
		data_entry.orp = json_obj['S2']
		data_entry.conductivity = json_obj['S3']
		data_entry.turbidity = json_obj['S4']
		data_entry.temperature = json_obj['S5']
		data_entry.flow_rate = json_obj['S6']

		data_entry.save()

def get_sensordata(request):

	global time_zone
	global is_server_connected
	global is_client_connected

	print 'JSON Request'

	json_obj = send_Data(b'r');

	if (json_obj):

		#Append to JSON object
		json_obj['is_client_connected'] = is_client_connected

	else:

		#Create JSON object
		json_obj = {'is_client_connected':is_client_connected}

	json_obj['is_server_connected'] = is_server_connected
	json_obj['date_time'] = datetime.now(time_zone).strftime('%H:%M %d/%m/%Y')

	return JsonResponse(json_obj)

def auto_system_check():

	global time_zone
	global system_fault

	threading.Timer(60, auto_system_check).start()

	print 'Auto System Check...'

	json_obj = send_Data(b'r');

	ph = 0.0
	orp = 0.0
	conductivity = 0.0
	turbidity = 0.0
	temperature = 0.0
	flow_rate = 0.0

	if (json_obj):

		ph = float(json_obj['S1'])
		orp = float(json_obj['S2'])
		conductivity = float(json_obj['S3'])
		turbidity = float(json_obj['S4'])
		temperature = float(json_obj['S5'])
		flow_rate = float(json_obj['S6'])

	fault_message = '\n'

	if (ph > 8.5):
		fault_message += '-pH above 8.5\n'
		system_fault = True

	if (ph < 6.5 and ph > 1):
		fault_message += '-pH below 6.5\n'		
		system_fault = True

	if (conductivity > 1250):
		fault_message += '-Conductivity above 1250 μS/cm\n'
		system_fault = True

	if (flow_rate > 0 and flow_rate < 2.5):
		fault_message += '-Flow rate low\n'
		system_fault = True

	if (temperature > 30):
		fault_message += '-Temperature above 30°C\n'
		system_fault = True

	if (turbidity > 1):
		fault_message += '-Turbidity above 1 NTU\n'
		system_fault = True

	if (system_fault):
		#send_email(True, fault_message)
		print'\nReported Fault(s):\n' + fault_message+'\n'

	system_fault = False


def send_email(isFault,fault_message):

	global recipient_email
	global sender_email
	
	if (isFault == False):

		subject_line = 'System Test'
		message = 'Dear Operator,\n\nThis is a test email.\n\nPlease do not reply to this email.'

	else:

		subject_line = 'System Warning'
		message = 'Dear Operator,\n\nA fault has been detected by the system.\nReported Fault(s):\n'+fault_message+'\n\nPlease do not reply to this email.'

	try:

		send_mail(subject_line, message, sender_email, [recipient_email],fail_silently=False)

	except Exception as e:

		print 'Error! No Internet connection!'

#Call auto_data_save to start timed thread
auto_data_save()

#Auto system check
auto_system_check()