from xpyfun import *;
from datawindow import *;

import Tkinter;

class DataTkWindow(DataWindow,Tkinter.Tk):
	def __init__(self,winname='rootwin',tkwin=None):
		DataWindow.__dict__['__init__'](self,winname);
		if tkwin is not None:
			self['guiroot']=tkwin;
		else:
			Tkinter.Tk.__dict__['__init__'](self);
			self['guiroot']=self;
			func=DataWindow.__dict__['_DataWindow__ginit']
			func(self);	
			#print type(func)
			self.setposition(10,10);
		#print "dir:\n",dir(datawindow.__dict__)
		#print "keys:\n",datawindow.__dict__.keys()
		
		