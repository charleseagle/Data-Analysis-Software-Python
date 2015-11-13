from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;

class Fr_SpectSetColValue(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('update');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('sourcedata');
		
		parameterframe=self['parameterframe'];
		self['formulastr']=StringVar();
		self['formulastr'].set("'y=y'");

		lg=Label(parameterframe,text="Formula");
		eg=Entry(parameterframe,textvariable=self['formulastr']);
		lg.grid(row=0,column=0);
		eg.grid(row=0,column=1);
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
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
		
		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.update(formulastr);
			spectnew.log({"Operation":"set column value","formulastr":formulastr});
			spectranew.insert(spectnew,k);
					
		spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
		#pylab.figure();
		XpyFigure();
		spectraall.plot();
		spectranew.plot('o');
		#pass;
		

