from xpyfun import *;
from xydiscretefun import *;
from nummatrixcsv import *;

import copy;
import pylab;
class NumDataSheet(XyDiscreteFun,NumMatrixCSV):
	def __init__(self,filename=None,dilimiter="\t",row_width_chosen=None):
		XyDiscreteFun.__dict__['__init__'](self);
		NumMatrixCSV.__dict__['__init__'](self,filename,dilimiter,row_width_chosen);
		
	def import_(self,filename=None):
		self.importcsv(filename);
		self.setupxy();
		
	def setupxy(self):
		num_matrix=self['num_matrix'];
		self['x']=num_matrix[:,0];
		self['y']=num_matrix[:,1];