from controlframe import *;
from xpyfun import *;
from datamenu import *;

import easygui;
import numpy;

from Tkinter import *;

class DataExplorerFrame(ControlFrame):
	def __init__(self,master=None,objname=None,datadict=None):
		#print 'type of arg datawindow', type(datawindow)
		ControlFrame.__dict__['__init__'](self,master,framename=objname);
		self['datadict']=datadict;
		
		self.__dinit();
		self.__ginit();
		if datadict is not None:
			self.exploredata(datadict,objname);
			
	def __dinit(self):
		self['datadictchain']=[];
		self['datadictnamechain']=[];
		self['keyschain']=[];
		self['dirlistbox']=None;
		self['contentlistbox']=None;
		
	def __ginit(self):
		#print self.keys()
		toolbar=self['toolbar'];
		b = Button(toolbar, text="Refresh", command=self.refresh)
		b.pack(side=LEFT)
		b.pack(side=LEFT)
		self.pack();
		
		lowerframe=Frame(self['self']);
		lowerframe.pack(fill=BOTH,expand=1,side=BOTTOM);
		self['lowerframe']=lowerframe;

		self['dirlistbox']=self.explistframe(lowerframe,"Folders",SINGLE,width=15);
		dlbox=self['dirlistbox'];
		dlbox.bind("<Double-Button-1>", lambda event:self.doubleclickdirlistitem(event));
		
		self['contentlistbox']=self.explistframe(lowerframe,"Contents",width=25);
		clbox=self['contentlistbox'];
		clbox.bind("<Double-Button-1>", lambda event:self.doubleclicklistitem(event))
		clbox.bind("<Button-1>", lambda event:self.singleclicklistitem(event))
		clbox.bind("<Button-3>", lambda event:self.rightclicklistitem(event));

	def exploredata(self,datadict,objname='/'):
		self['datadict']=datadict;
		#self['datadictchain'].append(datadict);
		self.refresh(objname);
		
	def gosub(self,datadict,objname="/"):
		objname=str(objname);
		
		L=len(self['datadictchain']);
		self['datadictchain'].append(datadict);
		self['datadictnamechain'].append(objname);
		
		if isinstance(datadict,dict):
			keys=datadict.keys();
		else:
			keys=range(len(datadict))
		self['keyschain'].append(keys);
		
		self['contentlistbox'].delete(0, END);
		for k in keys:
			#print i;
			value=datadict[k];
			#value=recoverdataobjclass(value);
			strline=str(k)+' '+str(type(value))+' '+str(numpy.shape(datadict[k]));
			if isinstance(value,dict):
				try:
					value.isdatobj();
					strline='[O]'+strline;
				except:	
					strline='[d]'+strline;
			elif isinstance(value,list):
				strline='[l]'+strline;
			self['contentlistbox'].insert(END,strline);
		self['dirlistbox'].insert(END,objname);
		#print "packed"
		#print "binded"
	
	
	def cutchain(self,ichain):
		L0=len(self['datadictchain'])
		#print L0, L
		datadict=None;
		datadictname=None;
		while len(self['datadictchain'])-1>ichain:
			datadict=self['datadictchain'].pop();
			datadictname=self['datadictnamechain'].pop();
			a=self['keyschain'].pop();
			self['dirlistbox'].delete(END);
			#a=self['listframechain'].pop();
			#a.destroy();
			#a=self['listboxchain'].pop();
			#a.destroy();
			#a=self['vscrollbarchain'].pop();
			#a.destroy();
			#a=self['hscrollbarchain'].pop();
			#a.destroy();
		#if ichain>=0:
		#	self['dirlistbox'].delete(END);
			#self.gosub(self['datadictchain'][-1],self['datadictnamechain'][-1]);
		
		#self['dirlistbox'].delete(END);
		#self['dirlistbox'].insert(
		return (datadict,datadictname)
#============================================================
#for handeling the events
#============================================================	
	def singleclicklistitem(self,event):
		#self['currentchainindex']=ichain;
		rootwin=self.getrootdatawin();
		#rootwin['ans']=self.getcurrentdatalist();
		#print ilist
		
	def doubleclicklistitem(self,event):
		ichain=self.getcurrentchainindex();
		#print "ichain:",ichain
		self.cutchain(ichain);
		data=self.getcurrentdatalist();
		if len(data)>0:
			data=data[0];
			if isinstance(data,dict) or isinstance(data,list):
				dataname=self.getcurrentdatanamelist();
				dataname=dataname[0];
				self.gosub(data,dataname);
			elif isstring(data):
				self.stdout(data);
			elif isnumeric(data):
				self.stdout(data);
			else:
				self.stdout(type(data));
			
	def doubleclickdirlistitem(self,event):
		selistrtup=self['dirlistbox'].curselection();
		selinumlist=[];
		for k in selistrtup:
			selinumlist.append(int(k));
		#print "selinumlist",selinumlist
		ichain=selinumlist[0];
		#print "dir ichain:",ichain
		datadict,datadictname=self.cutchain(ichain-1);
		self.gosub(datadict,datadictname);
		
	def rightclicklistitem(self,event):
		#self['currentchainindex']=ichain;
		menu = DataMenu(self)
		 
		
		menu.add_command(label="Refresh", command=self.refreshcurdir);
		menu.add_command(label="Export ascii", command=self.exportascii);
		menu.add_command(label="New directory", command=self.newdir)
		menu.add_command(label="Move to peer directory", command=self.move2peer)
		menu.add_command(label="Move to parent directory", command=self.move2parent)
		menu.add_separator();
		
		menu.add_command(label="Display", command=self.displaydata)
		menu.add_command(label="Delete", command=self.deldata)
		menu.add_command(label="Copy", command=self.copy2clipborad);
		menu.add_command(label="Paste", command=self.pastefromclipborad);
		
		datalist=self.getcurrentdatalist();
		datanamelist=self.getcurrentdatanamelist();
		#print "len:",len(datalist);
		if len(datalist)==1:
			menu.add_command(label="Rename", command=self.renamedata)
			data=datalist[0];
			dataname=datanamelist[0];
			#if isa(data,"DataObject","dataobject"):
			if isdatobj(data):
				menu=data.contextmenu(menu,dataname);
		menu.post(event.x_root, event.y_root)

#==============================================================
#getting the selected data 		
#==============================================================
	def getcurrentdatadict(self):
		ichain=self.getcurrentchainindex();
		return self['datadictchain'][ichain];
		
	def getcurrentupperdatadict(self):
		ichain=self.getcurrentchainindex();
		if ichain>0:
			return self['datadictchain'][ichain-1];
		else:
			return None;
	
	def getcurrentdatadictname(self):
		ichain=self.getcurrentchainindex();
		return self['datadictnamechain'][ichain]
			
	def	getcurrentdatalist(self):
		datalist=[];
		namelist=self.getcurrentdatanamelist();
		datadict=self.getcurrentdatadict();
		for n in namelist:
			if isinstance(datadict,list):
				n=int(n);
			datalist.append(datadict[n]);
		return datalist;
		
	def getcurrentdatanamelist(self):
		datadict=self.getcurrentdatadict();
		datanamelist=[];
		curkeys=self.getcurrentkeys();
		curselilist=self.getcurrentselectionlist();
		for i in curselilist:
			n=curkeys[i];
			if isinstance(datadict,list):
				n=int(n);
			datanamelist.append(n);
		return datanamelist;
		
	def getcurrentselectionlist(self):
		try:
			selistrtup=self['contentlistbox'].curselection();
			selinumlist=[];
			for k in selistrtup:
				selinumlist.append(int(k));
		except:
			import tkMessageBox;
			tkMessageBox.showerror('Box selection not found','Choose something first!');
		#print "getcurrentselectionlist",selinumlist
		return selinumlist;

	def getcurrentkeys(self):
		ichain=self.getcurrentchainindex();
		return self['keyschain'][ichain];
		
	"""
	def getcurrentlistbox(self):
		ichain=self.getcurrentchainindex();
		return self['listboxchain'][ichain];
	"""
	#def getcurrentlistframe(self):
	#	ichain=self.getcurrentchainindex();
	#	return self['listframechain'][ichain];
	def getcurrentchainindex(self):
		ichain=None;
		#try:
		#	ichain=self['currentchainindex'];
		#except:
		#	import tkMessageBox;
		#	tkMessageBox.showerror('List box not selected','Choose something first!');
		ichain=len(self['datadictchain'])-1;
		return ichain;

	def getcurrentdatapath(self):
		pathlist=self['dirlistbox'].get(0,END);
		pathstr=self.cget('text');
		for i in range(1,len(pathlist)):
			pathstr=pathstr+"/"+pathlist[i];
		return pathstr;
		
#============================================================================	
# for pushing-button data manipulation	
#============================================================================
	def displaydata(self):
		data=self.getcurrentdatalist();
		#print 'Displaying data...'
		#print data
		self.stdout("Display data...");
		self.stdout(data);
		
	def setdata(self):	
		datalist=self.getcurrentdatalist();
		datadict=self.getcurrentdatadict();
		datanamelist=self.getcurrentdatanamelist();
		if len(datalist)==1:
			data=datalist[0];
			dataname=datanamelist[0];
			a=DataObject();
			a[dataname]=data;
			if isstring(data):
				a.uiset(FieldNames=[dataname],FieldValues=[data],datatype='string');
				datadict[dataname]=a[dataname];
			elif isnumeric(data):
				a.uiset(FieldNames=[dataname],FieldValues=[data],datatype='numeric');
				datadict[dataname]=a[dataname];
		else:
			import tkMessageBox;
			tkMessageBox.showerror('Erorr in set data','Choose ONE item!');	
			
	def deldata(self):
		datadict=self.getcurrentdatadict();
		#datalist=self.getcurrentdatalist();
		datanamelist=self.getcurrentdatanamelist();
		L0=len(self['datadictchain'])
		#print L0, L
		
		ichain=self.getcurrentchainindex();
		import easygui;
		msg=[];
		msg.append('Are you sure to delete');
		for name in datanamelist:
			msg.append(name);
		L=len(msg);
		if L>10:
			msg=msg[0:10];
			msg.append('etc. '+str(L)+'items');
		#print msg;
		msg.append('?');
		if easygui.ynbox(msg,'Deleting...'):
			for dataname in datanamelist:	
				del datadict[dataname];
			datadict,datadictname=self.cutchain(ichain-1);
			self.gosub(datadict,datadictname);
	
	def copydata(self):
		import copy;
		datadict=self.getcurrentdatadict();
		datanamelist=self.getcurrentdatanamelist();
		datalist=self.getcurrentdatalist();
		for i in range(len(datalist)):
			data=datalist[i];
			try:
				data.isdatobj();
				inew=data.copy();
			except:				
				inew=copy.copy(data);
			datadict[datanamelist[i]+'copy']=inew;
		self.updatecurrentframe();
		
	def copy2clipborad(self):
		#import copy;
		
		rootwin=self.getrootdatawin();
		#rootwin['ans']=self.getcurrentdatalist();
		datadict=self.getcurrentdatadict();
		datadictname=self.getcurrentdatadictname();
		datanamelist=self.getcurrentdatanamelist();
		datalist=self.getcurrentdatalist();
		clipboard={};
		for dname in datanamelist:
			clipboard[dname]=datadict[dname];
			self.stdout(datadictname+':'+dname+" copied to clipboard.");
		rootwin['clipboard']=clipboard;
		
	def pastefromclipborad(self):
		import copy;
		rootwin=self.getrootdatawin();
		clipboard=rootwin.get("clipboard");
		datadict=self.getcurrentdatadict();
		datadictname=self.getcurrentdatadictname();
		if isinstance(clipboard,dict):
			for k in clipboard.keys():
				data=clipboard[k];
				try:
					datacopy=data.copy();
				except:
					datacopy=copy.copy(data);
				if datadict.has_key(k):
					keycopy=k+'copy';
				else:
					keycopy=k;
				datadict[keycopy]=datacopy;
				self.stdout(keycopy+' pasted to '+datadictname+" from clipboard.");
			self.updatecurrentframe();
		
	def renamedata(self):
		datadict=self.getcurrentdatadict();
		data=self.getcurrentdatalist()[0];
		dataname=self.getcurrentdatanamelist()[0];
		newdataname=easygui.enterbox("new name?","renaming in dataexplorer",dataname);
		if newdataname is not None:
			datadict[newdataname]=data;
			del datadict[dataname];
			self.updatecurrentframe();

	def newdir(self):
		datadict=self.getcurrentdatadict();
		dirnew=DataObject();
		newdirname=easygui.enterbox("new dir name?","creating dir","newdir");
		if newdirname is not None:
			datadict[newdirname]=dirnew;
			self.updatecurrentframe();
		
	def move2parent(self):
		datalist=self.getcurrentdatalist();
		datanamelist=self.getcurrentdatanamelist();
		parentdatadict=self.getcurrentupperdatadict();
		datadict=self.getcurrentdatadict();
		for i in range(len(datanamelist)):
			parentdatadict[datanamelist[i]]=datalist[i];
			del datadict[datanamelist[i]];
		self.updateparentframe();

	def move2peer(self):
		datadict=self.getcurrentdatadict();
		datanamelist=self.getcurrentdatanamelist();
		choicelist=[];
		for name in datadict.keys():
			data=datadict[name];
			if isinstance(data,dict):
				if datanamelist.count(name)==0:
					choicelist.append(name);
		targetdir=easygui.choicebox("pick the target dir","moving to peer directory",choicelist);
		if targetdir is not None:
			subdatadict=datadict[targetdir];
			for name in datanamelist:
				subdatadict[name]=datadict[name];
				del datadict[name];
			self.updatecurrentframe();	
# for updating the explorer
	
	def updatecurrentframe(self):
		#print "updatecurrentframe"
		#datadict=self.getcurrentdatadict()
		#frametitle=self.getcurrentlistframe().cget('text');
		#frametitle="Contents"
		datadict,datadictname=self.cutchain(self.getcurrentchainindex()-1);
		self.gosub(datadict,datadictname);
		#print "frametitle",frametitle
		
	def updateparentframe(self):
		#print "updatecurrentframe"
		ichain=self.getcurrentchainindex();
		datadict=self.getcurrentupperdatadict()
		#frametitle=self['listframechain'][ichain-1].cget('text');
		#frametitle="Contents"
		datadict,datadictname=self.cutchain(self.getcurrentchainindex()-2);
		self.gosub(datadict,datadictname);
		
	def refresh(self,objname="/"):
		self.cutchain(-1);
		self.gosub(self['datadict'],objname);
		
	def refreshdir(self,ichain):
		#datadict=self['datadictchain'][ichain];
		#listbox=self['listboxchain'][ichain];
		#frame=self['listframechain'][ichain];
		#frametitle=frame.cget('text');
		datadict,datadictname=self.cutchain(ichain-1);
		self.gosub(datadict,datadictname);
	
	def refreshcurdir(self):
		ichain=self.getcurrentchainindex();
		self.refreshdir(ichain);
		
	def exportascii(self):
		import os;
		datadict=self.getcurrentdatadict();
		datanamelist=self.getcurrentdatanamelist();
		datalist=self.getcurrentdatalist();
		fullnamechosen=easygui.filesavebox("Choose the filename","Exporting ascii",".asc");
		
		li=os.path.split(fullnamechosen);
		pname=li[0];
		fname=li[1];
		self.stdout( "Exporting...");
		for i in range(len(datalist)):
			data=datalist[i];
			dataname=datanamelist[i];
			fname=dataname+'_'+fname;
			fullnamechosen1=os.path.join(pname,fname);
			if isdatobj(data):
				data.exportascii(fullnamechosen,dataname);
			else:
				st=repr(data);
				f=open(fullnamechosen1,"w");
				f.write(st);
				f.close();
		self.stdout("Done.");
		
	def explistframe(self,master,framename,selectmode=EXTENDED,width=20):
		myframe=LabelFrame(master,text=framename);
		myframe.pack(side=LEFT,fill=BOTH,expand=1);
		myhsbar=Scrollbar(myframe,orient=HORIZONTAL);
		myhsbar.pack(side=BOTTOM,fill=X);
		mylistbox=Listbox(myframe,relief=SUNKEN,selectmode=EXTENDED,width=width);
		mylistbox.pack(side=LEFT, expand=YES, fill=BOTH);
		
		myvsbar=Scrollbar(myframe);
		myvsbar.pack(side=RIGHT,fill=Y);
		
		myvsbar.config(command=mylistbox.yview);
		myhsbar.config(command=mylistbox.xview);
		mylistbox.config(yscrollcommand=myvsbar.set,xscrollcommand=myhsbar.set);
		
		return mylistbox;