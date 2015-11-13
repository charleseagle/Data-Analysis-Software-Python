from xyzdiscretefun import *;
from xyzplot import *;
#from xydiscretefun import *;
from xpyfun import *;
from xyplotstyle import *;
import pylab;

class XyzPlotable(XyzDiscreteFun,XyzPlot):
	def __init__(self):
		XyzDiscreteFun.__dict__['__init__'](self);
		pass;
			
	def contextmenu(self,menu,dataname=''):
		menu=XyzDiscretefun.contextmenu(self,menu,dataname);
		menu=XyzPlot.contextmenu(self,menu,dataname);
		return menu;
