#!/usr/bin/python3


import requests
import csv
import os
import logging
from nunchuck import nunchuck
import sched, time
from threading import Timer

try:
    from queue import Queue
except ImportError:
    from Queue import Queue
from collections import namedtuple
import threading


TICK_TIME = 1

options ={}
options['access_token'] = '121a6946461321fd48f813e8cda6ce07'
options['csv_file'] = "/Users/drydyk/src/homedata/homedata.csv"

#ON OFF CCL

logger = logging.getLogger(__name__)
logger.handlers = []
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            try:
                debounced.t.cancel()
            except(AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()
        return debounced
    return decorator

class WebPowerSwitch(object):
	"""docstring for WebPowerSwitch"""
	def __init__(self):
		super(WebPowerSwitch, self).__init__()
		self.base_url = "http://admin:seebeck10@10.0.1.67/"
		requests.get(self.base_url + 'login.tgi', params={'Username':'admin', 'Password':'seebeck10'})

	def outlet(self,outlet,state):
		requests.get(self.base_url + "outlet", params={outlet:state})
# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
# r.status_code
# r.headers['content-type']
# r.encoding
# r.text
# r.json

class WioLink(object):
	"""docstring for WioLink"""
	def __init__(self, arg):
		super(WioLink, self).__init__()
		#self.arg = arg
		self.data_cols = ['time','quality','temp','pressure','humidity','celsius_degree','fahrenheit_degree']
		self.csv_file = options['csv_file']

	def getHomeData(self):

		house_data ={}
		house_data['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
		house_data['quality'] = requests.get('https://us.wio.seeed.io/v1/node/GroveAirqualityA0/quality', params = options).json()['quality']
		house_data['temp'] = requests.get('https://us.wio.seeed.io/v1/node/GroveBaroBMP085I2C0/temperature', params = options).json()['temperature']
		house_data['pressure'] = requests.get('https://us.wio.seeed.io/v1/node/GroveBaroBMP085I2C0/pressure', params = options).json()['pressure']
		house_data['humidity'] = requests.get('https://us.wio.seeed.io/v1/node/GroveTempHumD0/humidity', params = options).json()['humidity']
		house_data['celsius_degree'] = requests.get('https://us.wio.seeed.io/v1/node/GroveTempHumD0/temperature', params = options).json()['celsius_degree']
		house_data['fahrenheit_degree'] = requests.get('https://us.wio.seeed.io/v1/node/GroveTempHumD0/temperature_f', params = options).json()['fahrenheit_degree']

		return house_data

	def write_csv_row(self,data_row):

		if os.path.isfile(csv_file):
			outfile = open(csv_file,"a")
			writer = csv.writer(outfile)
		else:
			outfile = open(csv_file,"w")
			writer = csv.writer(outfile)
			writer.writerow(data_cols)

		data_row = []


		for i in data_cols:
			data_row.append(house_data[i])

		writer.writerow(data_row)
		outfile.close()

class Nunchuck(nunchuck):
	"""docstring for Nunchuck"""
	def __init__(self):
		super(Nunchuck, self).__init__()
		#self.arg = arg
		#self.scale(value,min,max,out_min,out_max)

		#self.scale(value,min,max,out_min,out_max)

class HomeData(object):
	"""docstring for MainLoop"""
	def __init__(self, tick_delay):
		super(HomeData, self).__init__()
		self.tick_delay = tick_delay
		self.power_switch = WebPowerSwitch()
		self.nunchuck = Nunchuck()
		#self.wio_link = WioLink()

#		self.scheduler.enter(self.tick_delay,1,self.check_buttons,())
		print("beginning loop")


	def check_buttons(self):
		print("checking button state")
		logger.error("Checking Button State")
		if self.nunchuck.button_c():
			self.power_switch.outlet("a","ON")
		elif self.nunchuck.button_z():
			self.power_switch.outlet("a","OFF")
		threading.Timer(TICK_TIME,self.check_buttons).start()
#		self.scheduler.enter(self.tick_delay,1,self.check_buttons,())

if __name__ == '__main__':
    h = HomeData(1)
    threading.Timer(TICK_TIME,h.check_buttons).start()

