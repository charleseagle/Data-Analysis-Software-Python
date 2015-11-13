from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
import numpy;
from xpyfigure import *;
from xpyfun import *;
import mathfunc as m;
from emwspectrum import *;
from tmp_pickrange import *;

class Fr_SpectFilmCorrection(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('filmcorrection');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('rawspectra');
		parameterframe=self['parameterframe'];
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['rfilm']=StringVar();
		self['rfilm'].set('0.1428571')
#		self['wlfix']=StringVar();
#		self["wlfix"].set('310');
		
		l=Label(parameterframe, text="rfilm");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['rfilm']);
		e.pack();
#		l=Label(parameterframe, text="wlfix");
#		l.pack(side=TOP);
#		e=Entry(parameterframe, textvariable=self['wlfix']);
#		e.pack();

	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		spectracorrected=spectranew.copy();
		spectra.plot();
		#print "spectranew type:",type(spectranew);
		
		rfilm=float(self['rfilm'].get());
#		wlfix=float(self['wlfix'].get());
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());

		fullfilechosen=easygui.fileopenbox('Please choose a file (Ref for opus) to open','Opeing a file...',"*");
		if fullfilechosen is not None:
			extstandard=EMWSpectrum(fullfilechosen);
			extstandard.import_();
			extstandard['xunit'].setcurrentunit("cm_1");
			
			refchosen=easygui.choicebox("choose the reference","calculating ratio",spectra.keys());
			if refchosen is not None:
				spect0=spectra[refchosen];
				filmthickness={};
				for k in spectra.keys():
					self.stdout(k);
					spectnew=spectra[k].copyxy();
					# find out the film thichness first
					specttemp=spectnew.copyxy();
					specttemp.pick(xmin,xmax);
					fthickness=[];
					for x in specttemp['x']:
						yreal300K=extstandard(x);
						wavelength=1e7/x;
						rsample=yreal300K**0.5;
						yratio=spectnew(x)/spectra[refchosen](x);
						ft=m.findfilmthickness(yratio,wavelength,rfilm,rsample);
						fthickness.append(ft);
					filmthickness[k]=mean(fthickness);
					print "filmthickness"
					print fthickness;
					print filmthickness[k]
					# then get the real reflectance
					
					for i in range(len(spectnew['x'])):
						x=spectnew['x'][i];
						wavelength=1e7/x;
						yraw=spectnew(x)/spectra[refchosen](x)*extstandard(x);
						yreal=m.findrsample(yraw,wavelength,filmthickness[k],rfilm);
						spectnew['y'][i]=yreal;
						
					spectranew.insert(spectnew,k);
				XpyFigure();
				spectranew.plot('o');
				database[0]['resultdatatablegroups'][igroup]=spectranew;

