from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
import copy;
from tmp_pickrange import *;

class Fr_SpectSumRule(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('sumrule');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('eps2');	
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['V0']=StringVar();
		self['V0'].set('259.1e-30')
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Unit cell volume");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['V0']);
		e.pack();
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		eps1=database[0]['resultdatatablegroups'][igroup];
		
		spa_neff=eps1.getemptyinstance();
		V0=float(self['V0'].get());
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());

		for k in eps1.keys():
			sp_neff,omegap=eps1[k].sumrule(V0,xmin,xmax);
			spa_neff[k]=sp_neff;
			
		database[0]['resultdatatablegroups'][igroup]=spa_neff;
		spa_neff.plot('o');