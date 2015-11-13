from datatoplevelwindow import *;
from Tkinter import *;
import pylab;
import easygui;

class PlotControlWin(DataToplevelWindow):
	def __init__(self,fignum=None,approotwin=None):
		needginit=self.pyfiginit(fignum,approotwin);
		tkwin=self.gettkwin()
		DataTkWindow.__dict__['__init__'](self,winname=tkwin.title(),tkwin=tkwin);
		if needginit:
			self.ginit();
			
	def __ginit(self):
		mainframe=self['mainframe'];
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