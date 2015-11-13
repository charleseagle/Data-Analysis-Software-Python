from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from tmp_pickrange import *;

class Fr_PeakInfoExpDecay(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('ExpDecay');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2analyze');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['method']=IntVar();
		self["method"].set(0);
		
		parameterframe=self['parameterframe'];
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
			#print xmin,xmax
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());
		#resolution=float(self['resolution'].get());
		
		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.pick(xmin,xmax);
			paras,tauerror=spectnew.expdecayfit();
			
			I0=paras[0];
			tau=paras[1];
			baseline=paras[2];
			
			spectnew['I0']=I0;
			spectnew['tau']=tau;
			spectnew['baseline']=baseline;
			spectnew['tauerror']=tauerror;
			
			#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
			
		spectm0=spectranew.uicolumn2xy(ycolumn='I0');
		spectm1=spectranew.uicolumn2xy(ycolumn='tau');
		spectm2=spectranew.uicolumn2xy(ycolumn='baseline');
		spectm3=spectranew.uicolumn2xy(ycolumn='tauerror');
		
		spectranew1=spectranew.getemptyinstance();
		spectranew1.insert(spectm0,'I0');
		spectranew1.insert(spectm1,'tau');
		spectranew1.insert(spectm2,'baseline');
		spectranew1.insert(spectm3,'tauerror');
		
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot();
		import xpyfigure;
		xpyfigure.XpyFigure();
		subplot(2,2,1);spectm0.plot();
		subplot(2,2,2);spectm1.plot();
		subplot(2,2,3);spectm2.plot();
		subplot(2,2,4);spectm3.plot();
		
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];
		resultdata['resultdatatablegroups'][igroup]=spectranew1;
		resultdata['savestr']="ExpDecayParas"
		database.append(resultdata);
		#pass;
