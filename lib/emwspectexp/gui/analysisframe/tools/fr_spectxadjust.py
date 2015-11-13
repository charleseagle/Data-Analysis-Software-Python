from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
from tmp_pickrange import *;
import easygui;
import pylab;

class Fr_SpectXAdjust(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('xadjust');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2fix');
		parameterframe=self['parameterframe'];

		self.gettmpdata("groupstr").set("'None'");
	
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		spectra.plot();
		#print "spectranew type:",type(spectranew);
		xmin=-1e100;
		xmax=1e100;
		for k in spectra.keys():
			spect=spectra[k];
			xmin=max(min(spect['x']),xmin);
			xmax=min(max(spect['x']),xmax);
			print "xmin,xmax:",xmin,xmax
		xarray=array([]);
		
		for k in spectra.keys():
			spect=spectra[k];
			xmin=max(min(spect['x']),xmin);
			xmax=min(max(spect['x']),xmax);
			x=spect['x'];
			I1=numpy.core.logical_and(x>=xmin, x<=xmax);
			x1=x[I1];
			print "xshape:",x1.shape
			xarray=numpy.hstack((xarray,x1));
			print "allxshape",xarray.shape
			
		xarrays=set(xarray);
		print "set len:",len(list(xarrays));
		xarray=array(list(xarrays));
		xarray.sort();
		print type(xarray);
		print xarray.shape;
		#pylab.plot(xarray);
		
		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			y=spectnew(xarray);
			spectnew['x']=xarray;
			spectnew['y']=y;
			spectnew.log({"Operation":"xadjust"});
				#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
				
		spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');
		#pass;
		

