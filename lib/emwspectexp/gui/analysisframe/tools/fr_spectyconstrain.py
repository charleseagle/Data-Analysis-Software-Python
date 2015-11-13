from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
from tmp_pickrange import *;
import easygui;
import pylab;

class Fr_SpectYConstrain(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('yconstrain');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2fix');
		parameterframe=self['parameterframe'];
		
		self['ymin']=StringVar();
		self['ymin'].set('0');
		self['ymax']=StringVar();
		self['ymax'].set('1');
		
		myframe=LabelFrame(parameterframe,text="Parameters");
		myframe.pack(side=LEFT);
		lo=Label(myframe,text="y min");
		lp=Label(myframe,text="y max");
		eo=Entry(myframe,textvariable=self['ymin'],width=10);
		ep=Entry(myframe,textvariable=self['ymax'],width=10);
		lo.grid(row=0,column=0);
		eo.grid(row=0,column=1);
		lp.grid(row=1,column=0);
		ep.grid(row=1,column=1);
		
		self.gettmpdata("groupstr").set("'None'");
	
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		spectra.plot();
		#print "spectranew type:",type(spectranew);

		ymin=float(self['ymin'].get());
		ymax=float(self['ymax'].get());
		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.yconstrain(ymin=ymin,ymax=ymax);
			spectnew.log({"Operation":"yconstrain","ymin":ymin,"ymax":ymax});
				#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
				
		spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');
		#pass;
		

