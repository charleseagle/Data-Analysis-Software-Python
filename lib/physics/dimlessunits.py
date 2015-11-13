from units import *;

class DimlessUnits(Units):
	def __init__(self,unitname="unitname"):
		Units.__dict__['__init__'](self);
		self['dict']={'dimensionless':unitname};
		self['defaultunit']='dimensionless';
		self['currentunit']="dimensionless";
		