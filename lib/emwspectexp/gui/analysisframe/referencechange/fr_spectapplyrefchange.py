from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
import numpy;
from xpyfigure import *;
from xpyfun import *;

class Fr_SpectApplyRefChange(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):		
		self.gettmpdata('savename').set('refchangeapplied');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('samplespectra');
		self.ginitsourcedataentry('refchangespectra');
		self.ginitsourcedataentry('splchangespectra');
		parameterframe=self['parameterframe'];
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");

	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectrarefchange=database[1]['resultdatatablegroups'][igroup];
		spectrefchange=spectrarefchange[spectrarefchange.keys()[0]];
		spectrasplchange=database[2]['resultdatatablegroups'][igroup];
		spectsplchange=spectrasplchange[spectrasplchange.keys()[0]];
		spectranew=spectra.getemptyinstance();
		spectra.plot();
		
		spectchangeratio=spectsplchange.copyxy();
		spectchangeratio.ratio(spectrefchange);
		changeratio=spectchangeratio.yerrmean();
		print "changeratio:", changeratio;
		#spectsplchange['yerr']=numpy.fabs(spectsplchange['y']);
		changeratio1=spectsplchange['y'].sum()/spectrefchange['y'].sum();
		print "flat mean changeratio",changeratio1
		
		levels=spectsplchange['levels'];
		values=levels.values();
		I=values.index(0);
		refchosen=levels.keys()[I];
		#print "refchosen",refchosen
		#print spectra.keys()
		
		for k in spectra.keys():
			#print "k:",k
			spectnew=spectra[k];
			spectnew=spectnew.copyxy();
			print len(spectnew['y']),len(spectrefchange['y']),len(spectra[refchosen]['y'])
			spectnew['y']=spectnew['y']-levels[k]*spectrefchange['y']*spectra[refchosen]['y']*changeratio;
			#spectnew1['y']=spectnew1['y']-levels[k]*spectrefchange['y']*spectra[refchosen]['y'];
			spectnew.log({"Operation":"applyrefchange"});
			spectranew.insert(spectnew,k);
			
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		database[1]['save']=False;
		database[2]['save']=False;
		XpyFigure();
		spectranew.plot('o');
		#pass;
	

