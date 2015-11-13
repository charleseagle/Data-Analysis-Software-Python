from approotwin import *; 
from frametabs import *;
from xyplotcontrolframe import *;
from xyzplotcontrolframe import *
from figurecontrolframe import *

import Tkinter;

class LabAppWin(AppRootWin):
	def __init__(self,Appname='Approot'):
		AppRootWin.__dict__['__init__'](self,Appname);
		self.__ginit();
		

		#chkhold.pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH)
		#chknewfig.pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH)
		#sbmarker.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH);
		#print 'changed 1'
		
	def __ginit(self):
		mainframe=self['mainframe'];
		"""
		tabfr=FrameTabs(mainframe,framename='Plotconfig');
		mainframe.add_screen(tabfr,'Plotconfig')
		
		self['plotconfigtabs']=tabfr;
		xyframe=XyPlotControlFrame(tabfr);
		tabfr.add_screen(xyframe,'x-y')
		#print 'x-y'
		xyzframe=XyzPlotControlFrame(tabfr);
		tabfr.add_screen(xyzframe,'x-y-z')
		#print 'x-y-z'
		figframe=FigureControlFrame(tabfr);
		tabfr.add_screen(figframe,'figure')
		
		self['xycontrol']=xyframe;
		self['xyzcontrol']=xyzframe;
		self['figcontrol']=figframe;
		"""
	def getxyplotstyle(self):
		return self['xycontrol'].getcfg();
	def getfigcfg(self):
		return self['figcontrol'].getcfg();