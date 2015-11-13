from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from xpyfigure import *;
from emwspectrum import *;

class Fr_SpectPhaseShift(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('phaseshift');
		self.ginitsourcedataentry('sourcedata');
		
		self['alpha']=StringVar();
		self['alpha'].set('-1.5')
		self['efree']=StringVar();
		self["efree"].set('1e6');
		self['lowmethod']=StringVar();
		self['lowmethod'].set("constant");
		
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Free electron energy (cm^{-1}) ");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['efree']);
		e.pack();
		l=Label(parameterframe, text="Interband power");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['alpha']);
		e.pack();
		l=Label(parameterframe, text="Low energy extrapolation method");
		l.pack(side=TOP);
		e=Entry(parameterframe,textvariable=self['lowmethod']);
		e.pack();
				
	def analyze(self,igroup):
		import time;
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		efree=float(self['efree'].get());
		alpha=float(self['alpha'].get());
		lowmethod=self['lowmethod'].get();
		#print efree,alpha,lowmethod;
		self.stdout((efree,alpha,lowmethod));
		
		for k in spectra.keys():
			#self.getrootdatawin().stdout(("k:",k));
			#print k;
			self.stdout(k);
			t=time.time();
			spect=spectra[k];
			statuslabel=self.gettoplevel()['statuslabel'];
			spectnew=spect.phaseshifts(efree,alpha,lowmethod,statuslabel);
			spectnew.log({"Operation:":"phaseshift","efree":efree,"alpha":alpha,"lowmethod":lowmethod})
			spectranew.insert(spectnew,k);
			spectnew.plot();
			#spectnew.show();
			#print "time taken:",time.time()-t;
			self.stdout(("time taken:",time.time()-t));
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');
			