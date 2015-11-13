from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;

class Fr_SpectManualRenorm(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):		
		self.gettmpdata('savename').set('renorm_manual');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('sourcedata');			
		
		parameterframe=self['parameterframe'];
		self['gainstr']=StringVar();
		self['gainstr'].set('1');
		self['shiftstr']=StringVar();
		self['shiftstr'].set('0');
		lg=Label(parameterframe,text="Gain");
		ls=Label(parameterframe,text="Shift");
		eg=Entry(parameterframe,textvariable=self['gainstr']);
		es=Entry(parameterframe,textvariable=self['shiftstr']);
		lg.grid(row=0,column=0);
		eg.grid(row=0,column=1);
		ls.grid(row=1,column=0);
		es.grid(row=1,column=1);
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
	def analyze(self,igroup):
		# to get the sourcedata
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		#the real calculation
		spectraall=database[0]['datalist'][0];
		spectraall.plot();
		#spectraall.show();
		pylab.grid(True);
		
		shift=eval(self['shiftstr'].get());
		gain=eval(self['gainstr'].get());
		
		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew['y']=spect['y']*gain+shift;
			spectnew.log({"Operation":"manualrenorm","gain":gain,"shift":shift});
			spectranew.insert(spectnew,k);
					
		spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
		#pylab.figure();
		XpyFigure();
		spectraall.plot();
		spectranew.plot('o');
		#pass;
		

