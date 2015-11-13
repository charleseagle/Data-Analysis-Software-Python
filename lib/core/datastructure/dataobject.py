from pylab import *;
from xpyfun import *;
from xos import *;
import easygui;
from Tkinter import *;

class DataObject(dict):
	def __init__(self,dic=None):
		if dic is not None:
			for k in dic.keys():
				self[k]=dic[k];
		pass;
		
	def uiset(self,message="Fill in values for the fields."
		, title="set dataobject"
		, FieldNames  = None
		, FieldValues = None
		, datatype= 'string'):
		
		#print "fnames",FieldNames,'fvalues',FieldValues
		
		if FieldNames is None and FieldValues is None:
			FieldNames=[];
			FieldValues=[];
			for key in self.keys():
				v=self[key];
				#print 'v',type(v)
				if (datatype=='string' and isstring(v)):
					FieldNames.append(key);
					FieldValues.append(self[key]);
				elif (datatype=='numeric' and isnumeric(v)):
					#print key,self[key]
					FieldNames.append(key);
					FieldValues.append(str(self[key]));
#					i=i+1;
#					print i;
				
		inputfieldValues =easygui.multenterbox(message, title, FieldNames, FieldValues);
		
		#print inputfieldValues
		#print type(inputfieldValues)
		#print str(inputfieldValues)
		if str(inputfieldValues)!='None':
			for i in range(0,len(FieldNames)):
				if datatype=='numeric':
					self[FieldNames[i]]=str2num(inputfieldValues[i]);
				elif datatype=='string':
					self[FieldNames[i]]=inputfieldValues[i];

	def uiexplore(self,parentdatawin=None,dataname=None):
		import dataexplorerwin as dew;
		a=dew.DataExplorerWin(parentdatawin);
		a.explore(self,dataname);
		return a;
		
	def set(self,key,value):
		self[key]=value;
		
	def assignalldata(self,andict):
		for key in andict.keys():
			self[key]=andict[key];
			
	def get(self,key):
		value=None;
		if self.has_key(key):
			value=self[key];
		return	value;

	def copy(self):
		import copy;
		return copy.deepcopy(self);
		
	def keys(self):
		klist=dict(self).keys();
		#print klist
		klistnew=[];
		for k in klist:
			if not k.startswith('_datobj_'):
				klistnew.append(k);
		klistnew.sort();
		return klistnew;
		
	def keysoftype(self,typename,modulename=None):
		numkeys=[];
		for key in self.keys():
			v=self[key];
			#print 'v',type(v)
			if isa(v,typename,modulename):
				numkeys.append(key);

	def numerickeys(self):
		numkeys=[];
		#print "allkeys:",self.keys();
		for key in self.keys():
			v=self[key];
			#print 'v',type(v)
			if isnumeric(v):
				#print "isnumeric"
				numkeys.append(key);
		return numkeys;
		
	def getemptyinstance(self):
		tpdict=typedict(self);
		cmd="import "+tpdict['modulename'];
		exec(cmd);
		cmd='newobj='+tpdict['modulename']+'.'+tpdict['typename']+'()';
		exec(cmd);
		return newobj;
		
	def	importlist(self,L):
		i=0;
		for l in L:
			self['l'+str(i)]=l;
			i=i+1;
			
	def values(self):
		L=[];
		for k in self.keys():
			if not k.startswith("_datobj_"):
				L.append(self[k]);
		return L;
		
	def copy2puredict(self):
		resultdict={};
		tpdict=typedict(self);
		resultdict['_datobj_modulename']=tpdict['modulename'];
		resultdict['_datobj_typename']=tpdict['typename'];
		
		for k in self.keys():
			v=self[k];
			#print "copy2puredict key:",k
			#print "type:",type(v)	
			if isa(v,"DataObject","dataobject") or isinstance(v,DataObject) or isdatobj(v):
				vdict=v.copy2puredict();
				#print "found dataobj"
			elif isinstance(v,dict):
				v['_datobj_modulename']="dataobject";
				v['_datobj_typename']="DataObject";
				vobj=self.recoverdataobjclass(v);
				vdict=vobj.copy2puredict();
				#print "found dict"
			elif isinstance(v,list):
				v1=v[:];
				v1obj=DataObject();
				v1obj.importlist(v1);
				v1dict=v1obj.copy2puredict();
				vdict=v1dict.values();
				#print "found list"
			else:
				vdict=v;
				#print "found other"
			resultdict[k]=vdict;
		return resultdict;	
		
	def convert2puredatobj(self):
		for k in self.keys():
			v=self[k];
			if isinstance(v,dict):
				vdatobj=self.recoverdataobjclass(v);
				vdatobj.convert2puredatobj();
			elif isinstance(v,list):
				v1=v[:];
				v1obj=DataObject();
				v1obj.importlist(v1);
				v1obj.convert2puredatobj();
				vdatobj=v1obj.values();
			else:
				vdatobj=v;
			self[k]=vdatobj;	
			
	def	recoverdataobjclass(self,s):
		answer=s;
		#print "=================in recoverdataobjclass"
		#print "from type:",type(s);
		#import dataobject;
		if isinstance(s,dict):
			if not isdatobj(s):
				if s.has_key('_datobj_modulename'):
					modulename=s['_datobj_modulename'];
					typename=s['_datobj_typename'];
				else: 
					s['_datobj_modulename']='dataobject';
					s['_datobj_typename']="DataObject";
				modulename=s['_datobj_modulename'];
				typename=s['_datobj_typename'];
				cmd='import '+modulename;
				exec(cmd);
				cmd='objvalue = '+modulename+'.'+typename+'()';
				#print 'newobjcmd2:',cmd
				exec(cmd);
				objvalue.assignalldata(s);
				answer=objvalue
			#print "return type:",type(objvalue);			
		#print "==================to type:",type(answer);		
		return 	answer;	
	
	def datopcompare(self,expression,value,fuzzy=None):
		for k in self.keys():
			_cmd=k+'=self[k]';
			exec(_cmd);
		expvalue=eval(expression);
		#print "expvalue:",expvalue,"value:",value
		
		if fuzzy is None:
			result=expvalue==value;
		else:
			result=abs(expvalue-value)<fuzzy;
		#print "datopcompare:",expvalue,value,fuzzy,result
		return result;
		
	def contextmenu(self,menu,dataname=None):
		rmaster=gettoplevelmaster(menu);
		#print "rmaster",type(rmaster)
		menu.add_separator();
		#print "contextmenu in dataobject"
		menu.add_command(label="Set string",command=lambda:self.uiset(datatype="string"));
		menu.add_command(label="Set numeric",command=lambda:self.uiset(datatype="numeric"));
		menu.add_command(label="Explore",command=lambda:self.uiexplore(rmaster,dataname));
		menu.add_command(label="Displog",command=lambda:self.displog(menu));
		menu.add_command(label="Data command",command=lambda:self.uidatacommand(menu));
		return menu;
		
	def isdatobj(self):
		return True;
		
	def exportascii(self,farg,dataname=''):
		x=XOS();
		if isinstance(farg,str):
			fname=x.filenameappend(farg,dataname);
			print "Exporting "+dataname+" [DataObject] to:",fname
			fh=open(fname,'w');
			passname='';
			#fname=farg;
		else:
			fh=farg;
			passname=dataname;
		for k in self.keys():
			v=self[k];
			#print "k:",k
			fh.write(k+" {\n");
			if isdatobj(v):
				v.exportascii(fh,passname+'_'+k);
			else:
				st=repr(v);
				fh.write(st);
			fh.write("}\n");
		if isinstance(farg,str):
			fh.close();
		
	def cleardata(self):
		for k in self.keys():
			del self[k];
	
	def log(self,info):
		import time;
		import xos;
		methodcall=xos.getcaller();
		if not self.has_key('_dataobj_log'):
			self['_dataobj_log']=[];
		if self['_dataobj_log'] is None:
			self['_dataobj_log']=[];
		record={};
		record['time']=time.time();
		record['info']=info;
		record['caller']=methodcall;
		#print self['_dataobj_log'];
		self['_dataobj_log'].append(record);
		
		
	def displog(self,menu=None):
		import time;
		#import traceback;
		#methodcall=traceback.extract_stack();
		#print "methodcall",methodcall[-1];
		#xprint(self['_dataobj_log'],menu);
		if self.has_key('_dataobj_log'):
			for record in self['_dataobj_log']:
				xprint(time.ctime(record['time']),menu);
				if record.has_key('caller'):
					xprint(record['caller'],menu);
				for k in record['info']:
					v=record['info'][k];
					xprint((k,v),menu);
					
	def uidatacommand(self,menu):
		samplecmds='Examples:\n';
		samplecmds=samplecmds+"menu.stdout(self.keys())\n";
		answer=easygui.enterbox(samplecmds,"Data command","menu.stdout(self.keys())");
		if answer is not None:
			cmd=answer;
			exec(cmd);
			self.log({"datacommand":cmd});
			menu.stdout(answer);
			
	def getfromlog(self,index,varname):
		record=self['_dataobj_log'][index]['info'];
		print record;
		if record.has_key(varname):
			return record[varname];
		else:
			return None;