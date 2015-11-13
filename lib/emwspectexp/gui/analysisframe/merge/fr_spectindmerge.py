from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from xpyfigure import *;
from tmp_internalstandard import *;

class Fr_SpectIndMerge(DataOperationFrame,Tmp_InternalStandard):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_InternalStandard.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('merge_ind');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('sourcedata');
		self.gettmpdata("groupstr").set("'Temperature'");

		parameterframe=self['parameterframe'];
		
		myframe=LabelFrame(parameterframe,text="parameters");
		myframe.pack(side=LEFT);
		
		self['gainorshift']=IntVar();
		
		r=Radiobutton(myframe, text="Gain", variable=self['gainorshift'],value=0);
		r.grid(row=0,column=0,sticky=W);
		r=Radiobutton(myframe, text="Shift", variable=self['gainorshift'],value=1);
		r.grid(row=0,column=1,sticky=W);
		
	def analyze(self,igroup):
		# to get the sourcedata
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
#======================================================================
#         the real calculation
#======================================================================
		gainorshift=self['gainorshift'].get();
		
		keys=spectra.keyssorted(["min(x)"]);
		nameofintstandard=self['nameofintstandard'].get();
		if keys.count(nameofintstandard)==0:
			nameofintstandard=keys[0];
			self['nameofintstandard'].set(keys[0]);

		canceled=False;
		spect0=spectra[keys[0]].copyxy();
		gainfactors={};
		gainfactors[keys[0]]=1;

		for i in range(1,len(keys)):
			#print "i:",i
			spect=spectra[keys[i]].copyxy();
			spect0start=spect0.copyxy();
			spectstart=spect.copyxy();
			satisfied=False;
			while not satisfied and not canceled:
				spect0=spect0start.copyxy();
				spect=spectstart.copyxy();
				
				pylab.hold(False);
				spect0.plot('b');
				pylab.hold(True);pylab.grid(True);
				spect.plot('r');
				
				#print "spect0:",spect0['y'];
				#print "spect:",spect['y'];
				
				x,y1,y2=spect0.getcommonxy(spect);
				dx=(max(x)-min(x))/4;
				maxy=max(max(y1),max(y2));
				miny=min(min(y1),min(y2));
				dy=(maxy-miny)/4;
				#print x;
				#print y1;
				#print y2;
				A0=(min(x)-dx,max(x)+dx,miny-dy,maxy+dy)
				if (A0[0]-A0[1] )*(A0[2]-A0[3])!=0:
					#print "A0:",A0,(A0[0]-A0[1] )*(A0[2]-A0[3])
					pylab.axis(A0);
				answer=easygui.boolbox("Choose the range for for merging","Individual merging",["OK","Cancel"]);
				if answer==1:
					A=pylab.axis();
					xmin=A[0];
					xmax=A[1];
					gainfactors[keys[i]]=spect0.indmerge(spect,xmin,xmax,gainorshift);
					spect0.plot('g');
					if (A0[0]-A0[1] )*(A0[2]-A0[3])!=0:
						pylab.axis(A0);
				else:
					canceled=True;
				if not canceled	:
					answer=easygui.buttonbox("Satisfied?","Individual merging",["Yes","No","Cancel"]);
					#print "answer:",answer
					if answer=="Yes":
						satisfied=True;
					elif answer=="Cancel":
						canceled=True;
			if canceled:
				break;
			
		if not canceled:
			index=keys.index(nameofintstandard);
			print "index,gain:",index,gainfactors
			print "gainorshift:",gainorshift
			print "nameofintstandard",nameofintstandard
			if gainorshift==0:
				spect0['y']=spect0['y']/gainfactors[keys[index]];
			elif gainorshift==1:
				spect0['y']=spect0['y']-gainfactors[keys[index]];
			spect0.log({"operation":"Fr_SpectIndMerge","standard":nameofintstandard});
			spectnew=spect0;
			spectranew.insert(spectnew,keys[0]+'merged');
			spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
			spectnew.plot('o');