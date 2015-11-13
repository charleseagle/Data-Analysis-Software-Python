from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from tmp_pickrange import *;

class Fr_SpectCull(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):		
		self.gettmpdata('savename').set('spectraculled');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2pick');			
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['resolution']=StringVar();
		self['resolution'].set("2");
		
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="resolution (cm_1)");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['resolution']);
		e.pack();
		
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
			#print xmin,xmax
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());
		resolution=float(self['resolution'].get());
		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.cull(resolution,xmin,xmax);
			spectnew.log({"Operation":"cull","resolution":resolution,"xmin":xmin,"xmax":xmax});
			#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
				
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');
		#pass;
	
