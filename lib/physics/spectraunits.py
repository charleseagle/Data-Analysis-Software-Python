from units import *;

class SpectraUnits(Units):
	def __init__(self):
		Units.__dict__['__init__'](self);
		self['dict']={'cm_1':'Frequency',"nm":"Wave length","eV":"Energy"};
		self['tolerancedict']={'cm_1':1e-10,"nm":1e-10,"eV":1e-10};
		self['defaultunit']='cm_1';
		self['currentunit']="cm_1";
		
	def nm2cm_1(self,x):
		return 1e7/x;
	
	def eV2cm_1(self,x):
		return x*1e7/1240;
		
	def cm_12nm(self,x):
		return 1e7/x;
	
	def cm_12eV(self,x):
		return x*1240/1e7;