from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from tmp_pickrange import *;

class Fr_SpectCumSum(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		print "before ginit"
		self.__ginit();
		print "ginit"
		Tmp_PickRange.ginit(self);
		print "tmp init"
		
	def __ginit(self):
		self.gettmpdata('savename').set('cum_sum');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('sourcedata');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		parameterframe=self['parameterframe'];
		self['formulastr']=StringVar();
		self['formulastr'].set("'y=y'");
		lg=Label(parameterframe,text="Formula");
		lg.pack();
		eg=Entry(parameterframe,textvariable=self['formulastr']);
		eg.pack();
		#lg.grid(row=0,column=0);
		#eg.grid(row=0,column=1);
		
		
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

		formulastr=eval(self['formulastr'].get());
		
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());

		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.update(formulastr);
			spectnew=spectnew.cumsum(xmin,xmax);
			spectnew.log({"Operation":"cum sum","formulastr":formulastr});
			spectranew.insert(spectnew,k);
					
		spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
		#pylab.figure();
		XpyFigure();
		spectraall.plot();
		spectranew.plot('o');
		#pass;
		

