from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from tmp_pickrange import *;

class Fr_SpectraRangePick(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('spectrapicked');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2pick');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
			#print xmin,xmax
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());
		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.pick(xmin,xmax);
			spectnew.log({"Operation":"pick","xmin":xmin,"xmax":xmax});
			#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');
		#pass;

