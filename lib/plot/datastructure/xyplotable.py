from xydiscretefun import *;
from xyplot import *;
#from xydiscretefun import *;
from xpyfun import *;
from xyplotstyle import *;
import pylab;

class XyPlotable(XyDiscreteFun,XyPlot):
	def __init__(self):
		XyDiscreteFun.__dict__['__init__'](self);
		pass;
			
	def contextmenu(self,menu,dataname=''):
		menu=XyDiscreteFun.contextmenu(self,menu,dataname);
		menu=XyPlot.contextmenu(self,menu,dataname);
		return menu;
