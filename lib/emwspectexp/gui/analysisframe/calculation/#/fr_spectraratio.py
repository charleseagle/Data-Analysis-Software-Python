from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;

class Fr_SpectraRatio(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):		
		self.gettmpdata('savename').set('spectraratio');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2calculate');			
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
	def analyze(self,igroup):
	# to get the sourcedata
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		refchosen=easygui.choicebox("choose the reference","calculating ratio",spectra.keys());
		if refchosen is not None:
			#spectra.plot();
			#pylab.grid(True);
			#print xmin,xmax
			spectref=spectra[refchosen];
			for k in spectra.keys():
				#if k!=refchosen:
				spect=spectra[k];
				spectnew=spect.copyxy();
				spectnew.divideby(spectref);
				#print "spectranew type after:", type(spectranew);
				spectranew.insert(spectnew,k);
			
			database[0]['resultdatatablegroups'][igroup]=spectranew;
			spectranew.plot();
			