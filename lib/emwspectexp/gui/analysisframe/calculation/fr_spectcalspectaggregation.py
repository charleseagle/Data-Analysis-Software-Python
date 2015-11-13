from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
from xpyfigure import *;
from xpyfun import *;
from tmp_pickrange import *;

import easygui;
import pylab;
import numpy;

class Fr_SpectCalSpectAggregation(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('aggspect');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['operatorstr']=StringVar();
		self['operatorstr'].set("spect['y'].mean()");
		
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Operation (e.g. spect['y'].mean())");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['operatorstr']);
		e.pack();
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		
		spectranew=spectra.getemptyinstance();
		
		#spectra.plot();
		#print "spectranew type:",type(spectranew);
		operatorstr=self['operatorstr'].get();
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());

		for k in spectra.keys():
			spect0=spectra[k];
			spect=spect0.copyxy();
			spect.pick(xmin,xmax);
			cmd=operatorstr;
			ys=eval(cmd);
			spect['agg']=ys;
			spectranew.insert(spect,k);
			
		spectagg=spectranew.uicolumn2xy(ycolumn='agg');
		spectagg.log({"operation":"spectaggregation","operator":operatorstr});
		spectranew1=spectranew.getemptyinstance();
		spectranew1.insert(spectagg,'agg');
		
				
		database[0]['resultdatatablegroups'][igroup]=spectranew1;
			
		XpyFigure();
		spectranew1.plot('o');
		#pass;
		

