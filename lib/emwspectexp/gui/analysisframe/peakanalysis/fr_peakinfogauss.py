from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from tmp_pickrange import *;

class Fr_PeakInfoGauss(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('Gausspeak');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2analyze');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['method']=IntVar();
		self["method"].set(0);
		
		parameterframe=self['parameterframe'];
		r=Radiobutton(parameterframe, text="Plain", variable=self['method'],value=0);
		r.pack(side=LEFT);
		r=Radiobutton(parameterframe, text="Base line", variable=self['method'],value=1);
		r.pack(side=LEFT);
		r=Radiobutton(parameterframe, text="Base line and slope", variable=self['method'],value=2);
		r.pack(side=LEFT);
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
			#print xmin,xmax
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());
		#resolution=float(self['resolution'].get());
		
		method=self['method'].get();
		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.pick(xmin,xmax);
			paras=spectnew.gaussfit(method=method);
			
			amp=paras[0];
			center=paras[1];
			sigma=paras[2];
			slope=paras[3];
			intercept=paras[4];
			
			spectnew['amp']=amp;
			spectnew['center']=center;
			spectnew['sigma']=sigma;
			spectnew['slope']=slope;
			spectnew['intercept']=intercept;
			
			#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
			
		spectm0=spectranew.uicolumn2xy(ycolumn='amp');
		spectm1=spectranew.uicolumn2xy(ycolumn='center');
		spectm2=spectranew.uicolumn2xy(ycolumn='sigma');
		spectm3=spectranew.uicolumn2xy(ycolumn='slope');
		spectm4=spectranew.uicolumn2xy(ycolumn='intercept');
		
		spectranew1=spectranew.getemptyinstance();
		spectranew1.insert(spectm0,'amp');
		spectranew1.insert(spectm1,'center');
		spectranew1.insert(spectm2,'sigma');
		spectranew1.insert(spectm3,'slope');
		spectranew1.insert(spectm4,'intercept');
		
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot();
		import xpyfigure;
		xpyfigure.XpyFigure();
		subplot(3,2,1);spectm0.plot();
		subplot(3,2,2);spectm1.plot();
		subplot(3,2,3);spectm2.plot();
		subplot(3,2,4);spectm3.plot();
		subplot(3,2,5);spectm4.plot();
		
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];
		resultdata['resultdatatablegroups'][igroup]=spectranew1;
		resultdata['savestr']="moments"
		database.append(resultdata);
		#pass;
