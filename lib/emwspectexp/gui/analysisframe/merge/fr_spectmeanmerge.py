from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;

class Fr_SpectMeanMerge(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('merge_mean');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('sourcedata');
		self.gettmpdata("groupstr").set("'None'");
		
		self['agroupstr']=StringVar();
		self['agroupstr'].set("'Temperature','Mag_Field'");
		#self['tolerance']=StringVar();
		#self['tolerance'].set("1");

		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Groupstr");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['agroupstr']);
		e.pack();
		#l=Label(parameterframe, text="Tolerance");
		#l.pack(side=TOP);
		#e=Entry(parameterframe, textvariable=self['tolerance']);
		#e.pack();
		
		
	def analyze(self,igroup):
		# to get the sourcedata
		database=self.gettmpdata('database')
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		agroupstr=self['agroupstr'].get();
		#tolerance=float(self['tolerance'].get());

		#the real calculation
		#groups=spectra.group("Temperature");
		agroupstr=eval('['+agroupstr+']');
		groups=spectra.group(agroupstr);
		print "group string:",agroupstr
		print "Num of groups:",len(groups)
		for g in groups:
			keys=g.keyssorted("min(x)");
			print "keys in group:",keys
			spect0=g[keys[0]].copyxy();
			for i in range(1,len(keys)):
				spect=g[keys[i]];
				spect0.meanmerge(spect);
			spectnew=spect0;
			spectranew.insert(spectnew,keys[0]);
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		#pylab.figure();
		spectranew.plot('o');
		#pass;
		

