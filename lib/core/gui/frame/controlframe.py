from Tkinter import *;
from datalabelframe import *;
from hastoolbar import *;

class ControlFrame(DataLabelFrame,HasToolBar):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataLabelFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
	
	def __ginit(self):
		self.toolbar_ginit(self);
				
	def getfilewin(self):
		topwin=self.gettoplevel();
		if isa(topwin,'FileWin','filewin'):
			return topwin;
		else:
			return topwin.master;
		
	def getfilewindataexplorer(self):
		filewin=self.getfilewin();
		return filewin.getdataexplorer();
	
	def logrun(self,cmd,args=None):
		if args is None:
			args=[];
		fwin=self.getfilewin();
		tpdict=typedict(self);
		#print "logrun"
		import time;
		l={};
		l['frame']=tpdict['typename'];
		l['status']='starting...'
		l['cmd']=cmd;
		l['args']=args;
		fwin.log(l);	
		t1=time.time();
		
		_cmd=cmd+'(';
		
		for i in range(len(args)):
			_cmd=_cmd+'args['+str(i)+'],';
		if len(args)>0:
			_cmd=_cmd[0:-1];
		_cmd=_cmd+')'
		#print '_cmd in runcmd:',_cmd
		exec(_cmd);
		
		l={};
		l['frame']=tpdict['typename'];
		l['status']='finished...'
		l['cmd']=cmd;
		l['args']=args;
		l['timespan']=time.time()-t1;
		fwin.log(l);
