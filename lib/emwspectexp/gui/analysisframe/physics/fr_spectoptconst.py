from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
import copy;
class Fr_SpectOptConst(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('phys');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('Reflectance');	
		self.ginitsourcedataentry('Phase shift');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
			
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		Re=database[0]['resultdatatablegroups'][igroup];
		Ph=database[1]['resultdatatablegroups'][igroup];
		
		spa_n=Re.getemptyinstance();
		spa_k=Re.getemptyinstance();
		spa_eps1=Re.getemptyinstance();
		spa_eps2=Re.getemptyinstance();
		spa_sigma=Re.getemptyinstance();
		spa_alpha=Re.getemptyinstance();
		
		for k in Re.keys():
			Respect=Re[k];
			Phspect=Ph[k];
			
			sp_n,sp_k,sp_eps1,sp_eps2,sp_sigma,sp_alpha=Respect.optfncs(Phspect);
			
			spa_n[k]=sp_n;
			spa_k[k]=sp_k;
			spa_eps1[k]=sp_eps1;
			spa_eps2[k]=sp_eps2;
			spa_sigma[k]=sp_sigma;
			spa_alpha[k]=sp_alpha;
			
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

		spa_n.plot('o');
		spa_k.plot('o');
		spa_eps1.plot('o');
		spa_eps2.plot('o');
		spa_sigma.plot('o');
		spa_alpha.plot('o');