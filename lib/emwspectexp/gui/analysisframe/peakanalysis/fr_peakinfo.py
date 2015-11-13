from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from tmp_pickrange import *;

class Fr_PeakInfo(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('spectramoments');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2analyze');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['baseline']=IntVar();
		self["baseline"].set(1);
		
		parameterframe=self['parameterframe'];
		c=Checkbutton(parameterframe, text="Base line ?", variable=self['baseline']);
		c.pack();
		
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
			m0=spectnew.nthmoment(0);
			m1=spectnew.nthmoment(1);
			m2=spectnew.nthmoment(2);
			spectnew['m0']=m0;
			spectnew['m1']=m1;
			spectnew['m2']=m2;
			
			#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
		spectm0=spectranew.uicolumn2xy(ycolumn='m0');
		spectm1=spectranew.uicolumn2xy(ycolumn='m1');
		spectm2=spectranew.uicolumn2xy(ycolumn='m2');
		
		spectranew1=spectranew.getemptyinstance();
		spectranew1.insert(spectm0,'m0');
		spectranew1.insert(spectm1,'m1');
		spectranew1.insert(spectm2,'m2');
		
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot();
		import xpyfigure;
		xpyfigure.XpyFigure();
		subplot(3,1,1);spectm0.plot();
		subplot(3,1,2);spectm1.plot();
		subplot(3,1,3);spectm2.plot();
		
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];
		resultdata['resultdatatablegroups'][igroup]=spectranew1;
		resultdata['savestr']="moments"
		database.append(resultdata);
		#pass;
