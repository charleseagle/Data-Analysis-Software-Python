from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from tmp_pickrange import *;
import xpyfigure

class Fr_GaussDeconv(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('spectradeconv');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2analyze');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['width']=StringVar();
		self["width"].set('10');
		self['ndeconv']=StringVar();
		self["ndeconv"].set('100');
		self['alphadeconv']=StringVar();
		self["alphadeconv"].set('0.1');
		parameterframe=self['parameterframe'];
		
		l=Label(parameterframe, text="Width");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['width']);
		e.pack();
		l=Label(parameterframe, text="N deconv");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['ndeconv']);
		e.pack();
		l=Label(parameterframe, text="alpha deconv");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['alphadeconv']);
		e.pack();
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		#print xmin,xmax
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());
		width=float(self['width'].get());
		Ndeconv=int(self['ndeconv'].get());
		alphadeconv=float(self['alphadeconv'].get());
		#resolution=float(self['resolution'].get());
		xpyfigure.XpyFigure();
		
		for k in spectra.keys():
			print "spect:",k
			hold(False);
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.pick(xmin,xmax);
			spectnew.plot();
			hold(True);
			
			spectgauss=spectnew.copyxy();
			dx=width/10.;
			xgauss=arange(-width*5,width*5+dx,dx);
			spectgauss['x']=xgauss;
			ygauss=exp(-xgauss**2/2/width**2);
			spectgauss['y']=ygauss/ygauss.sum()/dx;
			
			spectnew=spectnew.deconv(spectgauss,Ndeconv,alphadeconv);
			spectnew.plot('o');
			#show();
			#raw_input('pause.');
			#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
		
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		hold(False);
		spectranew.plot();
