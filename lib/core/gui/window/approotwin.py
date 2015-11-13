from datatkwindow import *; 

from Tkinter import *;
import os,easygui;

class AppRootWin(DataTkWindow):
	instance=None;
	def __init__(self,winname='Approot'):
		self['imagedir']="image";
		DataTkWindow.__dict__['__init__'](self,winname);
		#self['savabledata']={};
		self['filewinclasses']={'FileWin':'filewin'};
		self['xpypath']=None;
		self['asciipath']=None;
		self['approotdir']=os.path.abspath(os.path.curdir);
		
		#print "winname: ",self['winname']
		self.__ginit();
		AppRootWin.instance=self;
		
	def __ginit(self):
		self.addclassmenu('Application',"New file",self.new);
		self.addclassmenu('Application',"Open file from disk",self.open);
		toolmenu=self.menu('Tools');
		toolmenu.add_command(label="Find string in files",command=self.uifindinfile);
		
		self.wintitle();
		
		toolbar=self['toolbar'];
		iconnew=self.loadimage('document-new.png');
		b = Button(toolbar, image=iconnew, command=self.new);
		b.photo=iconnew;
		b.pack(side=LEFT);
		self['balloon'].bind(b, 'New file.')
		
		iconopen=self.loadimage('folder-open.png');
		b = Button(toolbar, image=iconopen, command=self.open);
		b.photo=iconopen;
		b.pack(side=LEFT);
		self['balloon'].bind(b, 'Open file.')
		
		iconlog=self.loadimage('accessories-text-editor_002.png');
		b = Button(toolbar, image=iconlog, command=self.uitextout);
		b.photo=iconlog;
		b.pack(side=LEFT);
		self['balloon'].bind(b, 'Output window.');
		
		self.uitextout();
	# for file win	
	
		m=self.addmenu(None,"Help","Homepage",self.homepage);
		self.bindballoon(m,"Download newest version of the software and manual here.");
		
	def print_(self,msg):
		import time;
		msgstr=repr(msg);
		self['stdout'].print_(msg);
		
	def stdout(self,msg):
		self.print_(msg);
		
	def new(self):
		success=0;
		filewinclasses=self['filewinclasses'];
		if len(filewinclasses.keys())==1:
			filewinclassname=filewinclasses.keys()[0];
			filewinmodname=filewinclasses[filewinclassname];
		else:
			selection=choicebox('File class','Please choose',filewinclasses.keys());
			if selection!=None:
				filewinclassname=filewinclasses[selection];
				filewinmodname=filewinclasses[filewinclassname];
		if filewinclassname is not None:
			cmd='import '+filewinmodname;
			#print cmd;
			exec(cmd);
			cmd='file_win='+filewinmodname+'.'+filewinclassname+'(self)';
			#print cmd
			exec(cmd);
			file_win.dispsavable();
			success=True;
		return success;
		
	def open(self):
		filewinclasses=self['filewinclasses'];
		loadpath=self['xpypath'];
		initialfile='*.xpy';
		if loadpath is not None:
			initialfile=os.path.join(loadpath,initialfile);
		filechosen=easygui.fileopenbox('Please choose a file to open','Opeing a file...',initialfile);
		if filechosen is not None:
			li=os.path.split(filechosen);
			self['xpypath']=(li[0]);
			import shelve;
			self.stdout(("Loading data from",filechosen));
			try:
				f=shelve.open(filechosen);
				savabledata=f['savabledata'];
				f.close();
			except:
				import xos;
				savabledata=xos.zippickload(filechosen);
			filewinclass=savabledata['filewinclass'];
			filewinclassname=filewinclass['typename'];
			filewinmodname=filewinclass['modulename'];
			cmd='import '+filewinmodname;
			#print cmd;
			exec(cmd);
			cmd='file_win='+filewinmodname+'.'+filewinclassname+'(self,li[1])';
			#cmd='file_win='+filewinclassname+'(self)';
			exec(cmd);
			#savabledataobj=recoverdataobjclass(savabledata);
			#savabledataobj.convert2puredatobj();
			savabledataobj=DataObject(savabledata);
			savabledataobj.convert2puredatobj();
			file_win.setsavabledata(value=savabledataobj);
			file_win['savepath']=li[0];
			#print 'savepath',file_win['savepth']
			file_win.wintitle();
			file_win.dispsavable();
			self.stdout("Done.");
			
			
	def uifindinfile(self):
		import os;
		initpath=os.path.abspath(os.path.curdir);
		dir2search=easygui.diropenbox("Choose the directory","Finding string in files",initpath);
		if dir2search is not None:
			str2find=easygui.enterbox("string 2 find?","Finding string in files","print");
			if str2find is not None:
				found=findindir(dir2search,str2find);
				for record in found:
					self.print_(record);
	
	def getalldatawin(self):
		datawinlist=[self];
		childwinlist=self.getsubwinlist();
		datawinlist=datawinlist+childwinlist;
		return datawinlist;
		
	def getdataexplorerlist(self):
		explorerlist=[];
		datawinlist=self.getalldatawin();
		for w in datawinlist:
			exp=w.getdataexplorer();
			if exp is not None:
				explorerlist.append(exp);
		return explorerlist;
		
	def getcurrentdataexplorer(self):
		currentexplorer=None;
		explorerlist=self.getdataexplorerlist();
		for e in explorerlist:
			if len(e.getcurrentdatalist())>0:
				currentexplorer=e;
		return currentexplorer;
		
	def homepage(self):
		import webbrowser;
		webbrowser.open_new_tab('http://xpydaov.spaces.live.com/');