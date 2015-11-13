from xpyfun import *;
from datawindow import *;

import Tkinter;

class DataToplevelWindow(DataWindow,Tkinter.Toplevel):
	def __init__(self,parentdatawin=None,winname='unnamed'):
		DataWindow.__dict__['__init__'](self,winname);
		Tkinter.Toplevel.__dict__['__init__'](self,parentdatawin['guiroot']);
		self['guiroot']=self;
		#print 'parent of toplevel',type(parentdatawin);
		#print 'parent got from child',type(self.winfo_parent())
		#print 'parent from cget',type(self.keys())
		#print 'parent from cget',type(self.master)
		
		func=DataWindow.__dict__['_DataWindow__ginit']
		func(self);	
		
		pos=parentdatawin.getposition();
		#print pos
		if isinstance(parentdatawin,Tkinter.Tk):
			x0=pos['x0']+pos['dx']+10;
			y0=pos['y0']#+pos['dy']-10;
		else:
			x0=pos['x0'];#+pos['dx']+10;
			y0=pos['y0']+pos['dy']+45;
		self.setposition(x0,y0);
		#print self.group();
		
		#self.group(parentdatawin)
		#print "grouptop",type(self.group());