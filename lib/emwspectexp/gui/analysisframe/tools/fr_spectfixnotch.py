from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
from tmp_pickrange import *;
import easygui;
import pylab;

class Fr_SpectFixNotch(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('notch');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2fix');
		parameterframe=self['parameterframe'];
		
		self['norder']=StringVar();
		self['norder'].set('1');
		self['npoints']=StringVar();
		self['npoints'].set('20');
		
		myframe=LabelFrame(parameterframe,text="Parameters");
		myframe.pack(side=LEFT);
		lo=Label(myframe,text="n order");
		lp=Label(myframe,text="n points");
		eo=Entry(myframe,textvariable=self['norder'],width=10);
		ep=Entry(myframe,textvariable=self['npoints'],width=10);
		lo.grid(row=0,column=0);
		eo.grid(row=0,column=1);
		lp.grid(row=1,column=0);
		ep.grid(row=1,column=1);
		
		self.gettmpdata("groupstr").set("'min(x)','max(x)','Temperature'");
	
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		spectra.plot();
		#print "spectranew type:",type(spectranew);
		
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());
		norder=float(self['norder'].get());
		npoints=float(self['npoints'].get());
		for k in spectra.keys():
			print "k:",k
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.fixnotch(xmin=xmin,xmax=xmax,norder=norder,npoints=npoints);
			spectnew.log({"Operation":"fixnotch","xmin":xmin,"xmax":xmax,"norder":norder,"npoints":npoints});
			#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
				
		spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');
		#pass;
		

