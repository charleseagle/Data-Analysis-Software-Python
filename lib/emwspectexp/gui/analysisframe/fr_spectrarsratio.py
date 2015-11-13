from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
import copy;
class Fr_SpectraRSRatio(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):		
		self.gettmpdata('savename').set('spectrarsratio');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('delta Sample');	
		self.ginitsourcedataentry('Ratio Reference');
	
	def groupdata(self,data):
		#print "groundata:",type(data)
		datalist=data.group(["min(x)","max(x)"]);
		return datalist;	
			
	def analyze(self,igroup):
	# to get the sourcedata
		resultdatagrouped=self.gettmpdata('resultdatagrouped');
		
		Sdiffs=resultdatagrouped[0]['datagroups'][igroup];
		Rratios=resultdatagrouped[1]['datagroups'][igroup];
		#print "Rratio",type(Rratios),Rratios.keys();
		spectranew=Sdiffs.getemptyinstance();
		
# -------------------------------------------------------------------------real analysis
		refchosen=easygui.choicebox("choose the reference","calculating rsratio",Sdiffs.keys());
		if refchosen is not None:
			#spectra.plot();
			#pylab.grid(True);
			#print xmin,xmax
			spectS0=Sdiffs[refchosen].copy();
			spectS0['y']=spectS0['ybak'];
			spectR0=Rratios[refchosen[0:-1]+"M"].copy();
			spectR0['y']=spectR0['ybak'];
			
			for k in Sdiffs.keys():
				#if k!=refchosen:
				spectsdiff=Sdiffs[k];
				k1=k[0:-1]+"M"
				spectrratio=Rratios[k1];
				
				#y=spectrratio['y'];
				#y=spectR0['y']
				y=(spectsdiff['y']*spectrratio['y']+spectS0['y'])/spectR0['y'];
				
				spectnew=spectsdiff.copy();
				spectnew['y']=copy.copy(y);
				#print "spectranew type after:", type(spectranew);
				spectranew.insert(spectnew,k);
			
			resultdatagrouped[0]['datagroups'][igroup]=spectranew;
			#resultdatagrouped.pop(1);
			spectranew.plot();
			