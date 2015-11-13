from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
import copy;
from tmp_pickrange import *;

class Fr_SpectPelletFit(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('PelletFit');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('TPellet');
		self.ginitsourcedataentry('TXystal');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
					
		parameterframe=self['parameterframe'];
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		TPellet=database[0]['resultdatatablegroups'][igroup];
		TXystal=database[1]['resultdatatablegroups'][igroup];
		
		spectranew=TPellet.getemptyinstance();
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());

		for k in TPellet.keys():
			spectP=TPellet[k];
			spectnew=spectP.copyxy();
			spectP1=spectP.copyxy();
			spectP1.pick(xmin,xmax);
			#Trspect=Tr[k];
			if len(TPellet.keys())==1:
				spectX=TXystal[TXystal.keys()[0]];
				spectX1=spectX.copyxy();
				spectX1.pick(xmin,xmax);
				
			sp_fit,dratio,ratio,shift,chi2=spectP1.pelletfit(spectX1);
			y=spectnew['y'];
			ynew=((y-shift)/ratio)**(1/dratio);
			spectnew['y']=y;
			spectranew[k]=spectnew;
			print "dratio:",dratio
			print "ratio:",ratio
			print "shift:",shift
			print "chi2:",chi2
			
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectP.plot();
		spectX.plot('r');
		spectranew.plot('o');
		