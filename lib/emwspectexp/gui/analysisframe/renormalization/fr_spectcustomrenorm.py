from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from tmp_pickrange import *;

class Fr_SpectCustomRenorm(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):		
		self.gettmpdata('savename').set('renorm_custom');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('sourcedata');			
		
		self['operatorstr']=StringVar();
		self['operatorstr'].set("spect['y'].mean()");
		
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Operation (e.g. spect['y'].mean())");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['operatorstr']);
		e.pack();
		
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
		
		operatorstr=self['operatorstr'].get();
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());
		
		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			cmd=operatorstr;
			ys=eval(cmd);
			spectnew['y']=spectnew['y']/ys;
			spectnew.log({"Operation":"customrenorm","operatorstr":operatorstr});
			spectranew.insert(spectnew,k);
					
		spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
		#pylab.figure();
		XpyFigure();
		spectraall.plot();
		spectranew.plot('o');
		#pass;
		

