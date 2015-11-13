from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
import copy;
class Fr_SpectFilmRT2nk(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('FromRT');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('Reflectance');
		self.ginitsourcedataentry('Transmittance');
		self.ginitsourcedataentry('n substrate');
		self.ginitsourcedataentry('k substrate');
		
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
			
		self['samplethickness']=StringVar();
		self['samplethickness'].set('1e-4')
		self['subthickness']=StringVar();
		self['subthickness'].set('1e-4');
		
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Sample thickness (meter)");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['samplethickness']);
		e.pack();
		l=Label(parameterframe, text="Substrate thickness (meter)");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['subthickness']);
		e.pack();
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		Re=database[0]['resultdatatablegroups'][igroup];
		Tr=database[1]['resultdatatablegroups'][igroup];
		nsub=database[2]['resultdatatablegroups'][igroup];
		ksub=database[3]['resultdatatablegroups'][igroup];		
		spa_n=Re.getemptyinstance();
		spa_k=Re.getemptyinstance();
		spa_eps1=Re.getemptyinstance();
		spa_eps2=Re.getemptyinstance();
		spa_sigma=Re.getemptyinstance();
		spa_alpha=Re.getemptyinstance();
		spa_chi2=Re.getemptyinstance();
		
		samplethickness=float(self['samplethickness'].get());
		subthickness=float(self['subthickness'].get());
		for k in Re.keys():
			Respect=Re[k];
			#Trspect=Tr[k];
			if len(Re.keys())==1:
				Trspect=Tr[Tr.keys()[0]];
				nsubspect=nsub[nsub.keys()[0]];
				ksubspect=ksub[ksub.keys()[0]];
				
			sp_n,sp_k,sp_eps1,sp_eps2,sp_sigma,sp_alpha,sp_chi2=Respect.optfuncsfromRTFilm(Trspect,samplethickness,nsubspect,ksubspect,subthickness);
			
			spa_n[k]=sp_n;
			spa_k[k]=sp_k;
			spa_eps1[k]=sp_eps1;
			spa_eps2[k]=sp_eps2;
			spa_sigma[k]=sp_sigma;
			spa_alpha[k]=sp_alpha;
			spa_chi2[k]=sp_chi2;
			
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];resultdata['resultdatatablegroups'][igroup]=spa_n;
		resultdata['savestr']="n"
		database[0]=resultdata;
		
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];resultdata['resultdatatablegroups'][igroup]=spa_k;
		resultdata['savestr']="k"
		database[1]=resultdata;
		
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];resultdata['resultdatatablegroups'][igroup]=spa_eps1;
		resultdata['savestr']="eps1"
		database.append(resultdata);
		
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];resultdata['resultdatatablegroups'][igroup]=spa_eps2;
		resultdata['savestr']="eps2"
		database.append(resultdata);
		
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];resultdata['resultdatatablegroups'][igroup]=spa_sigma;
		resultdata['savestr']="sigma"
		database.append(resultdata);
		
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];
		resultdata['resultdatatablegroups'][igroup]=spa_alpha;
		resultdata['savestr']="alpha"
		database.append(resultdata);

		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];
		resultdata['resultdatatablegroups'][igroup]=spa_chi2;
		resultdata['savestr']="chi2"
		database.append(resultdata);
		
		spa_n.plot('o');
		spa_k.plot('o');
		spa_eps1.plot('o');
		spa_eps2.plot('o');
		spa_sigma.plot('o');
		spa_alpha.plot('o');