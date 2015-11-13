from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;

class Fr_SpectraDiff(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):		
		self.gettmpdata('savename').set('spectradiff');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2calculate');			
	
	def groupdata(self,data):
		#print "groundata:",type(data)
		datalist=data.group(["min(x)","max(x)"]);
		return datalist;	
			
	def analyze(self,igroup):
		resultdatagrouped=self.gettmpdata('resultdatagrouped');
		spectra=resultdatagrouped[0]['datagroups'][igroup];
		spectranew=spectra.getemptyinstance();
		#print "spectranew type:",type(spectranew);
		
		# real analysis
		refchosen=easygui.choicebox("choose the reference","calculating diff",spectra.keys());
		if refchosen is not None:
			#spectra.plot();
			#pylab.grid(True);
			#print xmin,xmax
			spectref=spectra[refchosen];
			for k in spectra.keys():
				#if k!=refchosen:
				spect=spectra[k];
				spectnew=spect.copyxy();
				spectnew.subtract(spectref);
				#print "spectranew type after:", type(spectranew);
				spectranew.insert(spectnew,k);
			
			resultdatagrouped[0]['datagroups'][igroup]=spectranew;
			resultdatagrouped[0]['dataname']="";
			spectranew.plot();
			