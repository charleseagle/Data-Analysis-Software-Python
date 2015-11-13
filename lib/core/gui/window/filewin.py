from savablewin import *;
import time;
#from subfilewin import *;

import os,easygui,shelve;
class FileWin(SavableWin):
	def __init__(self,parentdatawin=None,winname='unnamed'):
		SavableWin.__dict__['__init__'](self,parentdatawin,winname);
		#self['savabledata']={};
		
		self['subfilewinclasses']={'SubFileWin':'subfilewin'};
		self['fileext']='.xpy';
		
		#self['savabledata']['dataofchildren']={};
		self['savabledata']['filewinclass']=typedict(self);
		self['savepath']=None;
		self.__ginit();
		
	def __ginit(self):
		self.addclassmenu('Filewin',"Save file to disk",lambda cmd='self.save':self.logrun(cmd));
		self.addclassmenu('Filewin',"Save file to disk as",lambda cmd='self.save',arg=[True]:self.logrun(cmd,arg));
		self.addclassmenu('Filewin',"Adjust extension window",self.adjextwin);
		
		toolbar=self['toolbar'];
		iconsave=self.loadimage('media-floppy.png');
		b = Button(toolbar, image=iconsave, command=lambda cmd='self.save':self.logrun(cmd));
		b.photo=iconsave;
		b.pack(side=LEFT);
		self['balloon'].bind(b,'Save file to disk');
		
		iconadjextwin=self.loadimage('format-indent-less.png');
		b = Button(toolbar, image=iconadjextwin, command=self.adjextwin);
		b.photo=iconadjextwin;
		b.pack(side=LEFT);
		self['balloon'].bind(b,'Goto analysis window.');
		
	# for saving to disk	
	def save(self,saveas=False):
		success=False;
		
		filename=self['winname'];
		initialfile=filename;
		savepath=self['savepath'];
		filechosen=None;
		if savepath is not None:
			initialfile=os.path.join(savepath,initialfile);
			if not saveas:
				filechosen=initialfile;
		if filechosen==None:
			filechosen=easygui.filesavebox('Please choose a file to save','Disksaving...',initialfile);
		if filechosen!=None:
			self.save2disk(filechosen);
			self.wintitle();
			success=True;
		return success;	
		
	def saveswp(self):
		success=False;
		filename=self['winname'];
		initialfile='swp'+filename;
		savepath=self['savepath'];
		if savepath is not None:
			initialfile=os.path.join(savepath,initialfile);
		filechosen=initialfile;
		self.save2disk(filechosen);	
		return True;
		
	# for child win	
	def new(self):
		success=0;
		childclasslist=self['subfilewinclasses'];
		if len(childclasslist)==1:
			childclassname=childclasslist[0];
		else:
			selection=choicebox('Child class','Please choose',childclasslist);
			if selection!=None:
				childclassname=childclasslist[selection];
		if childclassname!=None:
			childname=easygui.enterbox('Enter the childname','Creating child','child'+str(len(self['savabledata']['dataofchildren'])));
			if childname!=None:
				cmd='childwin='+childclassname+'(self,childname)';
				print cmd
				exec(cmd);
				self['savabledata']['dataofchildren'][childname]=childwin['savabledata'];
				success=True;
		return success;
		
	def open(self):
		dataofchildren=self['savabledata']['dataofchildren'];
		childnames={};
		childclasses={};
		choicelist=[];
		for i in dataofchildren.keys():
			choice=i+':  <'+dataofchildren[i]['class']+'>';
			choicelist.append(choice);
			childnames[choice]=i;
			childclasses[choice]=dataofchildren[i]['class'];
		selection=easygui.choicebox('Child class','Please choose',choicelist);
		if selection!=None:
			print 'selection:',selection,type(selection)
			childname=childnames[selection];
			childclassname=childclasses[selection];
			cmd='childwin='+childclassname+'(self,childname)';
			exec(cmd);
			childwin['savabledata']=dataofchildren[childname];
			
	# backend functionsk	
	def save2disk(self,filechosen):
		if not filechosen.endswith(self['fileext']):
			filechosen=filechosen+self['fileext'];
		
		li=os.path.split(filechosen);
		self['savepath']=li[0];
		self['winname']=li[1];
		
		backupfname=os.path.join(self['savepath'],'_'+self['winname']);
		try:
			os.remove(backupfname);
		except:
			self.stdout((backupfname,'not found'));
		try:
			os.rename(filechosen,backupfname);
		except:
			self.stdout(("Can not rename:",filechosen));
			
		self.stdout(("Saving data to",filechosen));
		t1=time.time();
		#f=shelve.open(filechosen,writeback=True);
		#print "writeback"
		savabledata=self['savabledata'];
		savabledict=savabledata.copy2puredict();
		t2=time.time();
		self.stdout(("Converted to dict:",t2-t1,"secs."));
		import xos;
		xos.zippicksave(savabledict,filechosen);
		#f['savabledata']=savabledict;
		#f.sync();
		#print "sync"
		#f.close();
		self.log({'cmd':'save','msg':'File saved to: '+filechosen});
		t3=time.time();
		self.stdout(("Saved to disk:",t3-t2,"secs; Total",t3-t1,"secs."));
		self.stdout(("Factor:",(t3-t1)/(t2-t1)));

	def getxpypath(self):
		return self.getparentdatawin()['xpypath'];
		
	def setxppath(self,pathstr):
		self.getparentdatawin()['xypath']=pathstr;
		
	def getasciipath(self):
		pwin=self.getparentdatawin();
		#print "pwin type",type(pwin);
		return self.getparentdatawin()['asciipath'];
		
	def setasciipath(self,pathstr):
		pwin=self.getparentdatawin();
		#print "pwin type",type(pwin);
		pwin['asciipath']=pathstr;
		
	def getextensionwin(self):
		extwin=None;
		import extensionwin;
		children=self.winfo_children();
		for chi in children:
			if isa(chi,'ExtensionWin','extensionwin'):
				extwin=chi;
		if extwin is None:
			extwin=extensionwin.ExtensionWin(self);
		return extwin;	
		
	def addextcontrol(self,ftypename,fmodulename=None):
		if fmodulename is None:
			fmodulename=ftypename.lower();
		extwin=self.getextensionwin();
		mainframe=extwin['mainframe'];
		page=mainframe.add(ftypename.replace('_',''));
		
		cmd='import '+fmodulename;
		exec(cmd);
		cmd='fr='+fmodulename+'.'+ftypename+'(page,ftypename)';
		#print cmd;
		exec(cmd);
		fr.pack(fill='both',expand=1);
		mainframe.setnaturalsize();
		#mainframe.add_tab(ftypename,fr);
		
		
	def adjextwin(self):
		extwin=self.getextensionwin();
		pos=self.getposition();
		#print pos
		x0=pos['x0'];#+pos['dx']+10;
		y0=pos['y0']+pos['dy']+45;
		extwin.setposition(x0,y0);
		#print "extwinstate",extwin.state();
		#extwin.state('normal')
		extwin.deiconify();