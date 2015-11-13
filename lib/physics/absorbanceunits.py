from units import *;

class AbsorbanceUnits(Units):
	def __init__(self):
		Units.__dict__['__init__'](self);
		self['dict']={'m^{-1}':'\\alpha'};
		self['defaultunit']='m^{-1}';
		self['currentunit']="m^{-1}";