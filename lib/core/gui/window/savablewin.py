from datatoplevelwindow import *; 

class SavableWin(DataToplevelWindow):
	def __init__(self,parentdatawin=None,winname='unnamed'):
		DataToplevelWindow.__dict__['__init__'](self,parentdatawin,winname);
		self.set('savabledata',DataObject());
		self['savabledata']['log']=[];
		self.__ginit();
	#def __ginit(self):
		#self.addclassmenu('savablewin',"Save",lambda cmd='self.save':self.logrun(cmd));
		#self.addclassmenu('savablewin',"Save as",lambda cmd='self.saveas':self.logrun(cmd));	
		#guiroot.bell();
	#def __ginit(self):
	def __ginit(self):
		#self.addmenu("SavableWin","Log",self.uilog);
		self.addclassmenu('Alldata',"Log",self.uilog);
		toolbar=self['toolbar'];
		iconlog=self.loadimage('start-here_003.png');
		b = Button(toolbar, image=iconlog, command=lambda:self.uitextout("Log"));
		b.photo=iconlog;
		b.pack(side=LEFT);
		self['balloon'].bind(b,'View log');
		
	def uilog(self):
		import textoutframe;
		mainframe=self['mainframe'];
		frames=mainframe['screenlist'];
		foundframe=False;
		#for f in frames:
		#	#print f
		#	if isa(f,'TextOutFrame','textoutframe'):
		#		foundframe=True;
		
		if not foundframe:
			lframe=textoutframe.TextOutFrame(mainframe,'Log');
			#lframe.disptextout();
			lframe['textoutlist']=self['savabledata']['log'];
			mainframe.add_screen(lframe,'Log');
			mainframe.setactive(-1);
			
	def save(self):
		print 'saving...'
	def saveas(self):
		print 'saving as...'
		
	def log(self,lg):
		import time;
		lg['time']=time.localtime();
		self['savabledata']['log'].append(lg);
		#print 'Logged:'
		#print lg;
		#print self['statuslabel']['text']
		self['statuslabel']['text']=str(lg['cmd']);
		
	def logrun(self,cmd,args=None):
		if args is None:
			args=[];
		#print "logrun"
		import time;
		l={};
		l['status']='starting...'
		l['cmd']=cmd;
		l['args']=args;
		self.log(l);	
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
		l['status']='finished...'
		l['cmd']=cmd;
		l['args']=args;
		l['timespan']=time.time()-t1;
		self.log(l);		
			
	def	uiquit1(self):
		import time,easygui;
		loglist=self['savabledata']['log'];
		foundsave=False;
		T='';
		for i in range(len(loglist)-1,0,-1):
			cmd=loglist[i]['cmd'];
			if cmd.find('save')!=-1:
				foundsave=True;
				T=loglist[i]['time'];
				break;
				
		if i<len(loglist)-1:
			if T=='':
				msg='It has never been saved.'
			else:
				tnow=time.localtime();
				msg='It is saved ';
				if (tnow.tm_year-T.tm_year)>0:
					msg=msg+str(tnow.tm_year-T.tm_year)+'year ';
				if (tnow.tm_mon-T.tm_mon)>0:
					msg=msg+str(tnow.tm_mon-T.tm_mon)+'month ';
				if (tnow.tm_yday-T.tm_yday)>0:
					msg=msg+str(tnow.tm_yday-T.tm_yday)+'day ';
				if (tnow.tm_hour-T.tm_hour)>0:
					msg=msg+str(tnow.tm_hour-T.tm_hour)+'hour ';
				if (tnow.tm_min-T.tm_min)>0:
					msg=msg+str(tnow.tm_min-T.tm_min)+'min ';
				if (tnow.tm_sec-T.tm_sec)>0:
					msg=msg+str(tnow.tm_sec-T.tm_sec)+'sec ';
			msg=msg+' do you want to save before quitting?'		
				
			choice=easygui.indexbox(msg,'Warning of quitting savable win',["Yes","No","Cancel"]);
			if choice==1:
				self['guiroot'].destroy();
			elif choice==2:
				self.save();
				self['guiroot'].destroy();	
		else:
			self['guiroot'].destroy();
	
	def setsavabledata(self,key=None,value=None):
		if key is None:
			self.set('savabledata',value);
		elif key is not None and value is not None:
			savabledata=self.get('savabledata');
			savabledata.set(key,value);
			self.set('savabledata',savabledata);
		
	def getsavabledata(self,key=None):
		if key is None:
			return self.get('savabledata');
		else:
			savabledata=self.get('savabledata');
			return savabledata.get(key);
			
	def dispsavable(self):
		exp=self.getdataexplorer();
		exp.refresh();
		exp.gosub(self['savabledata'],'savabledata');
