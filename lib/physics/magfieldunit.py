from units import *;

class MagFieldUnit(DataObject):
	def __init__(self):
		self['dict']={'T':'H'};
		self['tolerancedict']={'T':1e-10};
		self['defaultunit']="T";
		self['currentunit']="T";