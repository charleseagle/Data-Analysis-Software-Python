from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
import copy;

class Fr_ColorSpect(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		#Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('sumrule');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('alpha');	
		#self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
		self['Thickness']=StringVar();
		self['Thickness'].set('[1e-6,2e-6]')
		self['Brightness']=StringVar();
		self['Brightness'].set('1.')
		self['Background']=StringVar();
		self['Background'].set('0.')
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Sample Thickness");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['Thickness']);
		e.pack();
		l=Label(parameterframe, text="Brightness");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['Brightness']);
		e.pack();		
		l=Label(parameterframe, text="Background");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['Background']);
		e.pack();	
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		alpha=database[0]['resultdatatablegroups'][igroup];
		
		#spa_neff=eps1.getemptyinstance();
		thickness=eval(self['Thickness'].get());
		brightness=eval(self['Brightness'].get());
		background=eval(self['Background'].get());
		#thickness=ones([thicknessstr.size]);
		#i=0;
		#for t in thicknessstr:
		#	thickness[i]=float(t);
		#	i=i+1;
		#xmin=float(self['xminstr'].get());
		#xmax=float(self['xmaxstr'].get());
		
		colors={};
		for k in alpha.keys():
			c={};
			for t in thickness:
				R,G,B=alpha[k].alpha2color(t,brightness,normalize=True);
				print "RGB",R,G,B
				c[t]=array([R,G,B])+background;
			colors[k]=c;
			
		database[0]['resultdatatablegroups'][igroup]=colors;
		
		Array=ones([len(alpha.keys()),len(thickness),3]);
		i=0;
		for k in alpha.keys():
			j=0;
			for t in thickness:
				#print "colors[k][t][0]",colors[k][t][0];
				Array[i,j,0]=colors[k][t][0];
				Array[i,j,1]=colors[k][t][1];
				Array[i,j,2]=colors[k][t][2];
				j=j+1;
			i=i+1;
		#imshow(Array,origin='lower');
		imshow(Array,origin='lower',extent=[min(thickness),max(thickness),0,max(len(alpha.keys())-1,1)],aspect='auto',interpolation='nearest');
		xlabel('Sample Thickness (m)')