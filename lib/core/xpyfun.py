#==================================
# About to deprecate
#==================================
def typestrfull(s):
	t=str(type(s));
	I=t.find(' ')
	return t[I+2:-3];

def typestr(s):
	t=str(type(s));
	I=t.find(' ')
	t1=t[I+2:-2];	
	I=t1.find('.');
	while I!=-1:
#		print t1
		t1=t1[I+1:len(t1)];
		I=t1.find('.');
	return t1;

def num2str(n,format):
	return repr(n)
		
#=================================
# str operation
#=================================
def str2num(s):
#	print s;
	a= eval(s);
#	print a
	return a;


"""
	def isnumeric(s):
	tpdict=typedict(s);
	t=tpdict['typename'];
	#print "typename:",t
	if t=='int'or t=='long' \
		or t=='float' or t=='complex':
		return True;
	else:
		return False;
"""
def isnumeric(s):
	answer=True;
	try:
		s1=s+1;
		#print "added"
		try:
			s0=s[0]
			#print "array"
			answer=False;
		except:
			pass;
			#print "good!"
	except:
		answer=False;
	return answer;
		
def isstring(s):
	tpdict=typedict(s);	
	t=tpdict['typename'];
	if t=='str':
		return True;
	else:
		return False;

def str2varname(s):
	for s0 in s:
		if not ('a'<=s0<='z' or 'A'<=s0<='Z' or '0'<=s0<='9' or s=='_'):
			s=s.replace(s0,'_');
	return s;		
#=========================================	
# class type etc.
#=========================================
def typedict(s):
	import re;
	answer={};
	g=re.search("<(\S+) '(\S+)'>",str(type(s)));
	typeclass=g.group(1);
	answer['type']=typeclass;
	modandclass=g.group(2);
	try:
		I=modandclass.index('.');
		answer['modulename']=modandclass[0:I];
		answer['typename']=modandclass[I+1:];
	except:
		answer['typename']=modandclass;
	return answer;	
	
def isa(s,typename,modulename=None):
	#print "typestr",type(s)
	match=False;
	if modulename is not None:
		cmd="import "+modulename;
		#print cmd;
		exec(cmd);
		#cmd='match=isinstance(s,'+modulename+'.'+typename+')';
		cmd='match=isinstance(s,'+modulename+'.'+typename+')';
		#print cmd;
		exec(cmd);
		#print "match",match
	if not match:
		tpdict=typedict(s);
		#print "not match, try compare typename:",typename,tpdict['typename']
		match=(typename==tpdict['typename']);
	"""if not match:
		cmd="import "+modulename;
		exec(cmd);
		cmd="import "+tpdict['modulename'];
		exec(cmd);	cmd='match=isinstance(s,'+tpdict['modulename']+'.'+tpdict['typename']+')';
		exec(cmd);
		print cmd
		print "match itself",match
		
		cmd='match=isinstance(s,'+modulename+'.'+typename+')';
		exec(cmd);
		print cmd;
		print "match class",match
	"""	
	return match;
	
def isdatobj(v):
	try:
		expfun=v.isdatobj();
		isdatobj=True;
	except:
		isdatobj=False;
	return isdatobj;
	
"""def	recoverdataobjclass(s):
	answer=s;
	#print "=================in recoverdataobjclass"
	#print "from type:",type(s);
	import dataobject;
	if isinstance(s,dict):
		if not isa(s,"DataObject","dataobject"):
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
"""	
"""
def dataobj2dict(s):
	#print "-------------------in dataobj2dict"
	#print "from type",type(s)
	import dataobject;
	answer=s;
	if isinstance(s,dict):
		tpdict=typedict(s);
		#if isinstance(s,dataobject.DataObject) or tpdict['typename']=="DataObject":
		if isa(s,'DataObject','dataobject'):
		#print "found dataobject type"
			#print "tpdict:",tpdict
			dictvalue={};
			for k in s.keys():
				dictvalue[k]=s[k];
			dictvalue['_datobj_modulename']=tpdict['modulename'];
			dictvalue['_datobj_typename']=tpdict['typename'];
			answer=dictvalue;
		#print self[key]
	#print "---------------------return type",type(answer)
	return answer;
"""
# ====================================================
# mathematical functions
#=====================================================
def nonzeroarray(array,nzmin=None):
	import numpy;
	newarray=array.copy();
	
	Iz=newarray==0;
	Inz=newarray!=0;
	if nzmin is None:
		nzmin=min(numpy.fabs(newarray[Inz]));
	newarray[Iz]=nzmin;
	return newarray;
"""	
def xarange(x0,xend,dx):
	import numpy;
	a=numpy.arange(x0,xend,dx);
	N=int(round((xend-x0)/dx));
	#print "N:",N,"L:",len(a)
	if len(a)<N:
		a=numpy.hstack((a,xend-dx));
	elif len(a)>N:
		a=a[:-1];
	return a;
"""
#==============================================
# for tkinter
#==============================================
def gettoplevelmaster(tkwidget):
	import Tkinter;
	tkw=tkwidget;
	master=tkwidget.master;
	if master is not None:
		while not isinstance(master.master,Tkinter.Toplevel) and master.master is not None:
			tkw=master;
			master=master.master;
			#print "tkw type:",type(tkw);
			#print "master type:",type(master)
			#print "master.master type:",type(master.master)
		if isinstance(master.master,Tkinter.Toplevel):
			master=master.master;
	return master;

def stdout(msg):
	import approotwin;
	approot=approotwin.AppRootWin.instance;
	approot.stdout(msg);
	
def xprint(msg,widget=None):
	if widget is None:
		print msg;
	else:
		widget.stdout(msg);