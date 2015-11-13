from units import *;

class OptCondUnits(Units):
	def __init__(self):
		Units.__dict__['__init__'](self);
		self['dict']={'\\Omega^{-1}m^{-1}':'\\sigma_1'};
		self['defaultunit']='\\Omega^{-1}m^{-1}';
		self['currentunit']="\\Omega^{-1}m^{-1}";
		