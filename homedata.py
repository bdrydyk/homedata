#!/usr/bin/python3


import requests
import time
import csv
import os

data_file = "/Users/drydyk/src/homedata/homedata.csv"

class WebPowerSwitch(object):
	"""docstring for WebPowerSwitch"""
	def __init__(self):
		super(WebPowerSwitch, self).__init__()
		self.base_url = "http://10.0.1.67/"
		requests.get(self.base_url + 'login.tgi', params={'Username':'admin', 'Password':'seebeck10'})
		
r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
r.status_code
r.headers['content-type']
r.encoding
r.text
r.json

options ={}
options['access_token'] = '121a6946461321fd48f813e8cda6ce07'

#r = requests.get('https://us.wio.seeed.io/v1/node/GroveAirqualityA0/quality', )
house_data ={}
house_data['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
house_data['quality'] = requests.get('https://us.wio.seeed.io/v1/node/GroveAirqualityA0/quality', params = options).json()['quality']
house_data['temp'] = requests.get('https://us.wio.seeed.io/v1/node/GroveBaroBMP085I2C0/temperature', params = options).json()['temperature']
house_data['pressure'] = requests.get('https://us.wio.seeed.io/v1/node/GroveBaroBMP085I2C0/pressure', params = options).json()['pressure']
house_data['humidity'] = requests.get('https://us.wio.seeed.io/v1/node/GroveTempHumD0/humidity', params = options).json()['humidity']
house_data['celsius_degree'] = requests.get('https://us.wio.seeed.io/v1/node/GroveTempHumD0/temperature', params = options).json()['celsius_degree']
house_data['fahrenheit_degree'] = requests.get('https://us.wio.seeed.io/v1/node/GroveTempHumD0/temperature_f', params = options).json()['fahrenheit_degree']

data_cols = ['time','quality','temp','pressure','humidity','celsius_degree','fahrenheit_degree']

house_data

if os.path.isfile(data_file):
	outfile = open(data_file,"a")
	writer = csv.writer(outfile)
else:
	outfile = open(data_file,"w")
	writer = csv.writer(outfile)
	writer.writerow(data_cols)

data_row = []

for i in data_cols:
	data_row.append(house_data[i])

writer.writerow(data_row)
outfile.close()
