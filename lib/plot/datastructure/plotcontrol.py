#from numdatasheet import *;
from datatoplevelwindow import *;
from plotcontrolframe import *;
import pylab;

class PlotControl():
	def __init__(self):
		pass;
		
	def uiplot(self,menu):
		#print "get top from menu:"
		topwin=menu.gettoplevel();
		dataexplorer=topwin.getdataexplorer();
		dataname=dataexplorer.getcurrentdatanamelist()[0];
		datapath=dataexplorer.getcurrentdatapath();
		dataname=datapath+"/"+dataname;
		
		
		rootwin=menu.getrootdatawin();
		plotcontrolwin=rootwin.findchildwin('Plot Control');
		if plotcontrolwin==None:
			plotcontrolwin=DataToplevelWindow(rootwin,'Plot Control');
			page=plotcontrolwin.addpage("PlotControl");
			frame=PlotControlFrame(page);
		#print "PlotControlFrame"
			frame.pack(fill='both');
			plotcontrolwin['mainframe'].setnaturalsize();
			pos=topwin.getposition();
			plotcontrolwin.shiftposition(pos['dx']);
		else:
			frame=plotcontrolwin.findframeinnotebook("PlotControl");
		frame.adddata(dataname,self);
		
	def contextmenu(self,menu,dataname=''):
		import time,os;
		#menu=DataObject.__dict__['contextmenu'](self,menu);
		#menu.add_separator();
		menu.add_command(label="Add to plotlist",command=lambda:self.uiplot(menu));
		return menu;
