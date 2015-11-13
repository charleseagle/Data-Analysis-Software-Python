from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
import numpy;
from xpyfigure import *;
from xpyfun import *;

class Fr_SpectFindRefChange(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('refchange');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('refspectra');
		parameterframe=self['parameterframe'];
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");

	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		spectracorrected=spectranew.copy();
		spectra.plot();
		#print "spectranew type:",type(spectranew);
		
		refchosen=easygui.choicebox("choose the reference","calculating ratio",spectra.keys());
		if refchosen is not None:
			spect0=spectra[refchosen];
			spectradiff=spectranew.copy();
			for k in spectra.keys():
				spect=spectra[k];
				spectnew=spect.copyxy();
				if k!=refchosen:
					spectnew.diff(spect0);
					spectnew.ratio(spect0);
					spectradiff.insert(spectnew,k);
		
			ylist=spectradiff.aggselect('y');
			ymatrix=numpy.array(ylist);
			yerrlist=spectradiff.aggselect('yerr');
			yerrmatrix=numpy.array(yerrlist);
			yerrmatrix=nonzeroarray(yerrmatrix);
			
			ysign=(ymatrix.sum()).sum();
			print "ysign",ysign
			for i in range(len(ylist)):
				y=ylist[i];
				if ysign*y.mean()<0:
					y=-y;
					ylist[i]=y;
			ymatrix=numpy.array(ylist);
			ysign=(ymatrix.sum()).sum();
			print "ysign",ysign
			
			#ymatrixsqrt=numpy.sqrt(numpy.fabs(ymatrix));
			#ymatrixsqrt=nonzeroarray(ymatrixsqrt);
			#refy=(numpy.fabs(ymatrix)/ymatrixsqrt).sum(0)/(1/ymatrixsqrt).sum(0);
			#refy=(ymatrix/ymatrixsqrt).sum(0)/(1/ymatrixsqrt).sum(0);	
			#refy=(ymatrix).mean(0);
			refy=(ymatrix/yerrmatrix/yerrmatrix).sum(0)/(1/yerrmatrix/yerrmatrix).sum(0);
			spectrefchange=spectradiff[spectradiff.keys()[0]].copyxy();
			spectrefchange['y']=refy;
			
			#print "refy:",refy.shape
			#print refy
			spectraratio=spectranew.copy();
			keys=spectradiff.keys();
			levels={};
			levels[refchosen]=0;
			
			for k in keys:
				spect=spectradiff[k];
				spectnew=spect.copyxy();
				spectnew.ratio(spectrefchange);
				#print spectnew['yerr']
				levels[k]=spectnew.yerrmean();
				print k,levels[k]
				spectnew['y']=spectnew['y']-levels[k];
				spectraratio.insert(spectnew,k);
			spectrefchange['levels']=levels;
			
			for k in spectraratio.keys():
				spectnew=spectra[k].copyxy();
				spectnew['y']=spectnew['y']-levels[k]*spectrefchange['y']*spect0['y'];
				spectracorrected.insert(spectnew,k);
			spectracorrected.insert(spect0,refchosen);
			
			spectranew.insert(spectrefchange,refchosen+"_fx");
			database[0]['resultdatatablegroups'][igroup]=spectranew;
			
			if len(database)==1:
				record=database[0].copy();
				record['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];
				record['resultdatatablegroups'][igroup]=spectracorrected;
				record['savestr']="subtracted"
				database.append(record);
			else:
				database[1]['resultdatatablegroups'][igroup]=spectracorrected;
			
			XpyFigure();
			spectranew.plot('o');
			XpyFigure();
			spectracorrected.plot('o');
	

