from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
from tmp_pickrange import *;
import easygui;
import pylab;

class Fr_SpectFixGlich(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):		
		self.gettmpdata('savename').set('glich');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2fix');
		parameterframe=self['parameterframe'];
		self.gettmpdata("groupstr").set("'min(x)','max(x)','Temperature'");
	
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		spectra.plot();
		#print "spectranew type:",type(spectranew);

		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());

		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.fixglich(xmin=xmin,xmax=xmax);
			spectnew.log({"Operation":"fixglich","xmin":xmin,"xmax":xmax});
				#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
				
		spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');
		#pass;
		

