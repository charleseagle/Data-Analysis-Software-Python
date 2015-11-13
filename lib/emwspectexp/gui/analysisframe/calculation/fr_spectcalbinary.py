from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
from xpyfigure import *;
from xpyfun import *;

import easygui;
import pylab;
import numpy;

class Fr_SpectCalBinary(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('ratio');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra1');
		self.ginitsourcedataentry('spectra2');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['operatorstr']=StringVar();
		self['operatorstr'].set("+");
		
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Operator (e.g. + - * /)");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['operatorstr']);
		e.pack();
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectraspl=database[0]['resultdatatablegroups'][igroup];
		spectraref=database[1]['resultdatatablegroups'][igroup];
		
		spectranew=spectraspl.getemptyinstance();
		
		#spectra.plot();
		#print "spectranew type:",type(spectranew);
		print spectraref.keys()
		
		refchosen=easygui.choicebox("choose the second spectrum","binary calculation",spectraref.keys());
		if refchosen is not None:
			spectref=spectraref[refchosen];
			operatorstr=self['operatorstr'].get();
			for k in spectraspl.keys():
				spectnew=spectraspl[k];
				spectnew.binop(spectref,operatorstr);
				spectnew.log({"operation":"binop","operator":operatorstr});
				#spectnew.displog();
				spectranew.insert(spectnew,k);
				#spectranew[k].displog();
				
			database[0]['resultdatatablegroups'][igroup]=spectranew;
			database[1]['save']=False;
			
			XpyFigure();
			spectranew.plot('o');
		#pass;
		

