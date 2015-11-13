from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
from xpyfigure import *;
from xpyfun import *;

import easygui;
import pylab;
import numpy;

class Fr_SpectCalBinaryAuto(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('ratioauto');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra1');
		self.ginitsourcedataentry('spectra2');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['agroupstr']=StringVar();
		self['agroupstr'].set("'min(x)','max(x)','Temperature','Mag_Field'");
		
		self['operatorstr']=StringVar();
		self['operatorstr'].set("+");
		
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Operator (e.g. + - * /)");
		#l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['operatorstr']);
		#e.pack();
		
		l1=Label(parameterframe, text="Groupstr");
		#l.pack(side=TOP);
		e1=Entry(parameterframe, textvariable=self['agroupstr']);
		
		l.grid(row=0,column=0,sticky=W);
		e.grid(row=0,column=1,sticky=W);
		l1.grid(row=1,column=0,sticky=W);
		e1.grid(row=1,column=1,sticky=W);
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectraspl=database[0]['resultdatatablegroups'][igroup];
		spectraref=database[1]['resultdatatablegroups'][igroup];
		
		spectranew=spectraspl.getemptyinstance();
		
		agroupstr=self['agroupstr'].get();
		
		#spectra.plot();
		#print "spectranew type:",type(spectranew);
		print spectraref.keys()
		
#		refchosen=easygui.choicebox("choose the second spectrum","binary calculation",spectraref.keys());
#		if refchosen is not None:
		agroupstr=eval('['+agroupstr+']');
		operatorstr=self['operatorstr'].get();
		
		splgroups=spectraspl.group(agroupstr);
		refgroups=spectraref.group(agroupstr);
		print "group string:",agroupstr
		print "Num of groups:",len(splgroups)
		i=0;
		for splg in splgroups:
			splspect=splg[splg.keys()[0]];
			refg=refgroups[i];
			refspect=refg[refg.keys()[0]];
			
			spectnew=splspect.copyxy();
			spectranew.insert(spectnew,splg.keys()[0]);
			spectnew.binop(refspect,operatorstr);
			spectnew.log({"operation":"binop","operator":operatorstr});
			
			spectranew.insert(spectnew,splg.keys()[0]);
		#spectranew[k].displog();
		
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		database[1]['save']=False;
			
		XpyFigure();
		spectranew.plot('o');
		#pass;
		

