from numdatasheet import *;
from xyplot import *;
from xyzplot import *;
#from xydiscretefun import *;
from xpyfun import *;
from xyplotstyle import *;
from xpyfigure import *;
import pylab;

class NumDataSheetPlotable(NumDataSheet,XyPlot):
	def __init__(self,filename=None,dilimiter="\t",row_width_chosen=None):
		NumDataSheet.__dict__['__init__'](self,filename,dilimiter,row_width_chosen);
	
			
	def contextmenu(self,menu,dataname=''):
		menu=NumDataSheet.contextmenu(self,menu,dataname);
		menu=XyPlot.contextmenu(self,menu,dataname);
		return menu;
