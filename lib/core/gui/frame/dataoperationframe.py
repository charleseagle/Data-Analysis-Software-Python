from controlframe import *;
from xpyfigure import *;
from datalistframe import *;
from datalabelframe import *;
from Tkinter import *;
import easygui;

class DataOperationFrame(ControlFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		ControlFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__dinit();
		self.cleargroupdata();
		self.__ginit();
		
	def __dinit(self):
		self.settmpdata('savename',StringVar(self));
		self.gettmpdata('savename').set('savename');
		self.settmpdata('groupstr',StringVar(self));
		self.gettmpdata('groupstr').set("'None'");
		self.settmpdata('isourcedata',0);
		
		self.settmpdata('individual',IntVar());
		self.gettmpdata('individual').set(0);
		
		self.settmpdata('overwritedata',IntVar());
		self.gettmpdata('overwritedata').set(0);
		
		self.settmpdata('preprocessorreset',IntVar());
		self.gettmpdata('preprocessorreset').set(0);
		
	def cleargroupdata(self):
		self.settmpdata('database',[]);
		self.settmpdata('extraresultdata',{});
		self.settmpdata('groupnum',IntVar());
		#self.gettmpdata('groupnum').set(0);
		
	def __ginit(self):
		#==================== general GUI
		toolbar=self['toolbar'];
		b=self.addbutton(lambda: self.preprocessorreset(b),text="Preprocess");
		self.bindballoon(b,"Preprocess the data: e.g. group them according to the criteria");
		#b=self.addbutton(lambda cmd='self.reset':self.logrun(cmd),text="Reset");
		#self.bindballoon(b,"Reset the analysis");
		
		chk=Checkbutton(toolbar,text="Individual?",variable=self.gettmpdata('individual'));
		chk.pack(side=LEFT);
		self.bindballoon(chk,"Ckeck if the source is individual spectrum");
		
		l=Label(toolbar,text='Group criteria:');
		l.pack(side=LEFT);
		e = Entry(toolbar,width=16,textvariable=self.gettmpdata('groupstr'));
		e.pack(side=LEFT);
		self.bindballoon(e,"Grouping criteria, \n e.g. \n'Temperature' means the same temperature, 'min(x)' means same min(x) will be put in the same group");
				
		mainframe=Frame(self['self']);#,relief=GROOVE,borderwidth=2);
		mainframe.pack();
		sourceframe=LabelFrame(mainframe,text='All source data');#relief=GROOVE,borderwidth=2);
		sourceframe.pack(side=LEFT);
		self['sourceframe']=sourceframe;
		parameterframe=LabelFrame(mainframe,text="Parameters");#,relief=GROOVE,borderwidth=2);
		parameterframe.pack(side=RIGHT);
		self['parameterframe']=parameterframe;
		#lowerframe=Frame(self['self'],side=TOP);
		#self['lowerframe']=lowerframe;
		self.cleargroupgui();
		
	def cleargroupgui(self):
		self.cleargui('anaframe');
		listframes=self.gettmpdata('listframes');
		if listframes is not None:
			for listframe in listframes:
				listframe.cleardata();
				listframe.refresh();
				
		#self.settmpdata('currentgroupframe'
		self.gettmpdata('currentgroupframe')

	def cleargui(self,itemname):
		if self.gettmpdata(itemname) is not None:
			self.gettmpdata(itemname).quit();
			self.settmpdata(itemname,None);
	
	def ginitsourcedataentry(self,entryname):
		isource=self.gettmpdata('isourcedata');
		parentframe=self['sourceframe'];
		sourceframe=Frame(parentframe,relief=GROOVE,borderwidth=2);
		sourceframe.pack(fill=BOTH,side=LEFT);
		
		listframe=DataListFrame(sourceframe,framename=entryname);
		listframe.pack(side=RIGHT);
		#print "hlv"
		listframe['listbox'].configure(height=3);
		
		b=Button(sourceframe,text='>>',command=lambda:self.setdata2sourcedataentry(listframe,isource));
		b.pack(side=LEFT);
		self.settmpdata('isourcedata',isource+1);
		self.bindballoon(b,"Add data from the explorer into analysis");
		
		listframes=self.gettmpdata("listframes");
		if listframes is None:
			listframes=[];
		listframes.append(listframe);
		self.settmpdata('listframes',listframes);
		
	def setdata2sourcedataentry(self,listframe,isource):
		database=self.gettmpdata('database');
		databaserecord={};
		dataexplorer=self.getfilewindataexplorer();
		
		#print 'dataexplorer type',type(dataexplorer)
		databaserecord['upperdatadict']=dataexplorer.getcurrentupperdatadict();
		databaserecord['datadict']=dataexplorer.getcurrentdatadict();
		databaserecord['datadictname']=dataexplorer.getcurrentdatadictname();
		databaserecord['datalist']=dataexplorer.getcurrentdatalist();
		databaserecord['datanamelist']=dataexplorer.getcurrentdatanamelist();
		databaserecord['save']=True;
		
		#listframe.configure(text=databaserecord['datadictname']);
		listframe.cleardata(); 
		listframe.refresh();
		for dataname in databaserecord['datanamelist']:
			listframe.addline(dataname);
		while len(database)<=isource:
			database.append(None);
		database[isource]=databaserecord;
		print type(databaserecord['datalist'])
	
	def setupsourcedatatable(self):
		database=self.gettmpdata("database");
		if self.gettmpdata('individual').get()==0:
			for record in database:
				record['sourcedatatable']=record['datalist'][0];
		else:
			for record in database:
				olddatadict=record['datadict'];
				olddatanamelist=record['datanamelist'];
				record['datadict']=record['upperdatadict']
				record['datanamelist']=[record['datadictname']];
				
				newdata=olddatadict.getemptyinstance();
				#print "oldtype",type(olddatadict)
				#print "type",type(newdata)
				#print record['datanamelist']
				for name in olddatanamelist:
					newdata[name]=olddatadict[name];
				record['sourcedatatable']=newdata;
		
	def getresultdataname(self):
		return self['resultdatanameentry'].get();
		
	def preprocessorreset(self,button):
		porr=self.gettmpdata('preprocessorreset').get();
		if porr==0:
			if self.preprocess():
				button.configure(text='Reset');
				self.gettmpdata('preprocessorreset').set(1);
		else:
			if self.reset():
				button.configure(text='Preprocess');
				self.gettmpdata('preprocessorreset').set(0);
			
			
	def preprocess(self):
		emptylist=False;
		listframes=self.gettmpdata('listframes');
		for listframe in listframes:
			if len(listframe['data'].keys())==0:
				emptylist=True;
		if not emptylist:
			self.setupsourcedatatable();
			self.groupdatalist();
			self.dispgroup();
		else:
			easygui.msgbox('Error: empty source data.');
		return  not emptylist;
		
	def reset(self):
		self.cleargroupdata();
		self.cleargroupgui();
		return True;
	def analyze(self,igroup):
		pass;
		
	def save(self):
		#print "saving to filewin"
		database=self.gettmpdata('database');
		for record in database:
			savename=self.getresultdataname()+record['savestr'];
			if record['save']:
				if self.gettmpdata('overwritedata').get()==1:
					record['datadict'][savename]=record['resultdatatable'];
				else:
					if record['datadict'].has_key(savename):
						record['datadict'][savename].merge(record['resultdatatable']);
					else:
						record['datadict'][savename]=record['resultdatatable'];
				print savename, " is saved. "

	def groupdatalist(self):
		database=self.gettmpdata('database');
		for record in database:
			#print "datakey:",record.keys()
			datatable=record['sourcedatatable'];
			datagroups=self.groupdata(datatable);
			#print "ngroup",len(datagroups)
			record['sourcedatatablegroups']=datagroups;
		self.source2resultgroup();
		
	def source2resultgroup(self):
		database=self.gettmpdata('database');
		i=0;
		for record in database:
			record['resultdatatablegroups']=record['sourcedatatablegroups'][:];
			record['savestr']=str(i);
			i=i+1;
		
	def resetgroup(self):
		database=self.gettmpdata('database');
		igroup=self.gettmpdata('groupnum').get();
		for record in database:
			record['resultdatatablegroups'][igroup]=record['sourcedatatablegroups'][igroup];
		
	def groupdata(self,datatable):
		#print "groupdata"
		groupstr=self.gettmpdata('groupstr').get();
		groupcriterialist=eval('['+groupstr+']');
		#print "groupstr:",groupstr,groupcriterialist
		self.stdoutrun(lambda: datatable.group(groupcriterialist));
		#try:
		datatablegroups=datatable.group(groupcriterialist);
		#except:
		#	self.stdout();
		#print len(datatablegroups)
		return datatablegroups;
	
	def dispgroup(self):
		recordlist=self.gettmpdata('database');
		spectralist=recordlist[0]['resultdatatablegroups'];
		anaframe=DataLabelFrame(self,'Analysis: '+str(len(spectralist))+' data groups');
		anaframe.pack(fill=BOTH);
		self.settmpdata('anaframe',anaframe);
			
		#command frame
		cmdframe=Frame(anaframe);
		cmdframe.grid(row=0,column=0);
		cmdbar=Frame(cmdframe);
		cmdbar.pack(side=TOP,fill=BOTH);
		groupoptions=range(len(spectralist));
		self.gettmpdata('groupnum').set(groupoptions[0]) # default value
		optgroupnum= apply(OptionMenu, (cmdbar, self.gettmpdata('groupnum')) + tuple(groupoptions))
		optgroupnum.pack(side=LEFT);
		self.bindballoon(optgroupnum,text='Current group number');
			
		b=Button(cmdbar,text='<<',command=lambda: self.changegroup(-1));
		b.pack(side=LEFT);
		self.bindballoon(b,"Previous group");
			
		b=Button(cmdbar,text='>>',command=lambda: self.changegroup(1));
		b.pack(side=LEFT);
		self.bindballoon(b,"Next group");
		
		b=Button(cmdbar,text="Analyze",command=lambda cmd="self.analyzegroup":self.logrun(cmd));
		b.pack(side=LEFT);
		self.bindballoon(b,"Analyze current group");
		
		b=Button(cmdbar,text="Reset",command=lambda cmd="self.resetgroup":self.logrun(cmd));
		b.pack(side=LEFT);
		self.bindballoon(b,"Reset current group data.");
			
		allcmdbar=Frame(cmdframe);
		allcmdbar.pack(side=BOTTOM,fill=BOTH);
		b=Button(allcmdbar,text="Reset all",command=lambda cmd="self.source2resultgroup":self.logrun(cmd));
		self.bindballoon(b,"Reset data for all groups");
			
		b.pack(side=LEFT);
		b=Button(allcmdbar,text="Join data",command=lambda cmd="self.finishanalysis":self.logrun(cmd));
		#b=Button(cmdbar,text="finish",command=self.finishanalysis);
		b.pack(side=LEFT);
		self.bindballoon(b,"Put all data from groups together");
		igroup=self.gettmpdata('groupnum').get();
		self.dispgroupcontent(igroup);
		
		topwin=self.gettoplevel();
		topwin['mainframe'].setnaturalsize();
	
	def dispgroupcontent(self,igroup):
		anaframe=self.gettmpdata('anaframe');
		if anaframe.get('currentgroupframe') is None:
			currentgroupframe=DataLabelFrame(anaframe,framename='Group#'+str(igroup));
			currentgroupframe.grid(row=0,column=1,rowspan=2);
			glistframe=DataListFrame(currentgroupframe,framename='Data list');
			glistframe.pack();
			glistframe['listbox'].configure(height=2,width=18);
			anaframe.set('currentgroupframe',currentgroupframe);
			anaframe.set('currentgroupdatalistframe',glistframe);
			
		currentgroupframe=anaframe.get('currentgroupframe');
		currentgroupframe.configure(text='Group#'+str(igroup));
		
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		#spectra=database[0]['resultdatatablegroups'][igroup];
		
		glistframe=anaframe.get('currentgroupdatalistframe');
		glistframe.configure(text=str(len(spectra.keys()))+' item');
		glistframe.cleardata();
		glistframe.refresh();
		for k in spectra.keys():
			print "key:",k
			glistframe.addline(k);
		
	
	def analyzegroup(self):
		igroup=self.gettmpdata('groupnum').get();
		self.analyze(igroup);
		print "Done."
		
	def changegroup(self,nchange):
		spectralist=self.gettmpdata('database')[0]['sourcedatatablegroups'];
		L=len(spectralist);
		groupnum=self.gettmpdata('groupnum').get();
		groupnum=groupnum+nchange;
		if groupnum>=L:
			groupnum=groupnum-L;
		elif groupnum<0:
			groupnum=groupnum+L;
		self.gettmpdata('groupnum').set(groupnum);
		self.dispgroupcontent(groupnum);
		
	def finishanalysis(self):
		database=self.gettmpdata('database');
		for record in database:
			record['resultdatatable']=self.mergegroups(record['resultdatatablegroups']);
		anaframe=self.gettmpdata('anaframe');
		if anaframe.get('savebar') is None:
			savebar=DataLabelFrame(anaframe);
			savebar.grid(row=1,column=0,sticky=W);
			anaframe.set('savebar',savebar);
		
			l=Label(savebar,text='Result:');
			l.grid(row=0,column=0);
			e = Entry(savebar,width=16,textvariable=self.gettmpdata('savename'));
			e.grid(row=0,column=1);
			self['resultdatanameentry']=e;
			b = Button(savebar, text="Save", command=lambda cmd='self.save':self.logrun(cmd))	#self.logrun)
			b.grid(row=1,column=0);
			chk=Checkbutton(savebar,text="Overwite?",variable=self.gettmpdata('overwritedata'));
			chk.grid(row=1,column=1);
			self.bindballoon(chk,"Ckeck if you want to overwrite the database.");
		
		topwin=self.gettoplevel();
		topwin['mainframe'].setnaturalsize();

	def gettmpdata(self,key=None):
		return self.get(key);
		
	def settmpdata(self,key=None,value=None):
		return self.set(key,value);
		
	def mergegroups(self,groups):
		allgroup=groups[0].getemptyinstance();
		for g in groups:
			allgroup.merge(g);
		return allgroup;
		
	def cutresultlist(self):
		pass;