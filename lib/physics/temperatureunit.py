from units import *;

class TemperatureUnit(DataObject):
	def __init__(self):
		self['dict']={'K':'temperature'};
		self['tolerancedict']={'K':1e-10};
		self['defaultunit']="K";
		self['currentunit']="K";