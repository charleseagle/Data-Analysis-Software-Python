from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from xpyfigure import *;


class Fr_SpectAllMerge(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):		
		self.gettmpdata('savename').set('merge_ind');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('sourcedata');			

		
	def analyze(self,igroup):
		# to get the sourcedata
		resultdatagrouped=self.gettmpdata('resultdatagrouped');
		
		spectra=resultdatagrouped[0]['datagroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		fig=XpyFigure();
#======================================================================
#         the real calculation
#======================================================================
		Tgroups=spectra.group(["Temperature"]);
		
		canceled=False;
		satisfied=False;
		pylab.hold(False);
		while not satisfied and not canceled:
			keys=Tgroups[0].keyssorted(["min(x)"]);
			j=0;
			for Tspectra in Tgroups:
				spect0=Tspectra[keys[0]];
				for i in range(1,len(keys)):
			#=======================================display:
					spect=Tspectra[keys[i]];
					spect0.plot('b');
					pylab.hold(True);pylab.grid(True);
					spect.plot('r');
					answer=easygui.boolbox("Choose the range for for merging","Individual merging",["OK","Cancel"]);
					if answer==1:
						A=pylab.axis();
						xmin=A[0];
						xmax=A[1];
				for Tspectra in Tgroups:
					spect0=Tspectra[keys[0]].copyxy();
					for i in range(1,len(keys)):
						spect=Tspectra[keys[i]];
						spect0.indmerge(spect,xmin,xmax);
						spect0.log({"Operation":"indmerge","xmin":xmin,"xmax":xmax});
					spectnew=spect0;
					
				spect0.plot('g');
			else:	
				canceled=True;
			if not canceled:
				answer=easygui.buttonbox("Satisfied?","Individual merging",["Yes","No","Cancel"]);
					#print "answer:",answer
				if answer=="Yes":
					satisfied=True;
				elif answer=="Cancel":
					canceled=True;
			if canceled:
				break;
					
		spectnew=spect0;	
		spectranew.insert(spectnew,keys[0]);
		spectra=resultdatagrouped[0]['datagroups'][igroup]=spectranew;
		#pylab.figure();
		spectranew.plot('o');
		#pass;
		

