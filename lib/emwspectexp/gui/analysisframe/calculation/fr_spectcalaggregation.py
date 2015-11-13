from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
from xpyfigure import *;
from xpyfun import *;

import easygui;
import pylab;
import numpy;

class Fr_SpectCalAggregation(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('ratio');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['agroupstr']=StringVar();
		self['agroupstr'].set("Temperature");
		self['operatorstr']=StringVar();
		self['operatorstr'].set("mean");
		self['tolerance']=StringVar();
		self['tolerance'].set("1");
		
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Groupstr");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['agroupstr']);
		e.pack();
		l=Label(parameterframe, text="Tolerance");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['tolerance']);
		e.pack();
		l=Label(parameterframe, text="Operation (e.g. mean,max,min,sum)");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['operatorstr']);
		e.pack();
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		
		spectranew=spectra.getemptyinstance();
		
		#spectra.plot();
		#print "spectranew type:",type(spectranew);
		agroupstr=self['agroupstr'].get();
		operatorstr=self['operatorstr'].get();
		tolerance=float(self['tolerance'].get());
		
		spectrag=spectra.group(agroupstr,_fuzzy=tolerance);
		#print "# of groups:",len(spectrag)
		for sps in spectrag:
			ys=[];
			if len(sps.keys())<=1:
				k=sps.keys()[0];
				spect=sps[k];
			else:
				#print "key len:",len(sps.keys());
				for k in sps.keys():
					#print "k:",k
					spect=sps[k];
					ys=ys+[spect['y']];
				ys=numpy.vstack(tuple(ys));
				#print "shape",ys.shape
				cmd=operatorstr+"(ys,0)";
				ys=eval(cmd);
				spect['y']=ys;
				#print "type:",type(ys)
				#print "len(ys):",len(ys)
			spectnew=spect;
			spectnew.log({"operation":"aggregation","operator":operatorstr});
			
			spectranew.insert(spectnew,k);
				#spectranew[k].displog();
				
			database[0]['resultdatatablegroups'][igroup]=spectranew;
			
		XpyFigure();
		spectranew.plot('o');
		#pass;

