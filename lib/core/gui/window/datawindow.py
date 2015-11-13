from xpyfun import *;
from dataobject import *;
from datawidget import *;
from hastoolbar import *;
#from frametabs import *;
from datamenu import *;

import Tkinter;
import Pmw;

class DataWindow(DataWidget,HasToolBar):
	def __init__(self,winname='unnamed'):
		self['winname']=winname;
		self['menubar']=None;
		self['Libclassmenu']=None;
		self['mainframe']=None;
		self['statusbar']=None;
		self['statuslabel']=None;
		self['dataexplorerframeclass']={'modulename':'dataexplorerframe','typename':'DataExplorerFrame'};
		
	def __ginit(self):
		guiroot=self['guiroot'];
		guiroot.protocol("WM_DELETE_WINDOW", self.uiquit)
		self['balloon']=Pmw.Balloon(guiroot);
		self.toolbar_ginit(guiroot);
		self.__menus();
		self.__frames();
		self.settitle();
		self['guiroot'].resizable(width=1,height=0);
		
	def settitle(self,windescription=''):
		wintype='<'+typestr(self).title()+'>';
		winpath=self.getdatawinpathstr();
		#print "settitle"
		#print 'winpath:',winpath
		self['guiroot'].title(self['winname']+wintype+': '+winpath+": "+windescription);
			
	def wintitle(self):
		self.settitle();
		
	def __menus(self):
		guiroot=self['guiroot'];
		menubar = Tkinter.Menu(guiroot);#,relief=Tkinter.SUNKEN,bw=1
		self['menubar']=menubar;
		
		classmenu = Tkinter.Menu(menubar, tearoff=0)
		classmenu.add_command(label="Exit", command=self.uiquit);
		
		menubar.add_cascade(label='File', menu=classmenu)
		self['Libclassmenu']=classmenu;
		guiroot.config(menu=menubar);
		
		self.addclassmenu('Alldata',"Set string data",self.uisetstr);
		self.addclassmenu('Alldata',"Set numeric data",self.uisetnum);
		self.addclassmenu('Alldata',"display keys",self.dispkeys);
		self.addclassmenu('Alldata',"Explore data",self.uiexploredata);
		#self.addclassmenu('Alldata',"Exit",guiroot.destroy);

	def	__frames(self):
		# toolbar
		b=self.addbutton(self.uiexploredata,text="Explorer",imagefname='system-file-manager.png');
		self['balloon'].bind(b,'DataExplorer');
		#print "datawin children",self.winfo_children()
		
		#statusbar
		statusbar = Tkinter.Frame(self['guiroot']);
		self['statusbar']=statusbar;
		statusbar.pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH);
		
		l=Tkinter.Label(statusbar, text=" statusbar", bd=1, relief=Tkinter.SUNKEN, anchor=Tkinter.W)
		l.pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH);
		self['statuslabel']=l;
		
		# mainframe
		#mainframe = FrameTabs(self['guiroot'],framename='');
		mainframe=Pmw.NoteBook(self['guiroot'],);
		#mainframe.configure(lowercommand=mainframe.setnaturalsize);
		self['mainframe']=mainframe;
		#mainframe.pack(fill=Tkinter.X, padx=50, pady=50);
		mainframe.pack(fill=Tkinter.BOTH)
		#mainframe.setnaturalsize();

	def addclassmenu(self,menugroupelabel,menulabel=None,menucommandfunc=None):
		return self.addmenu(self['Libclassmenu'],menugroupelabel,menulabel,menucommandfunc);
		
	def addmenu(self,parentmenu,menugroupelabel,menulabel=None,menucommandfunc=None):
		#print "menugroupelabel",menugroupelabel,"menulabel",menulabel
		if parentmenu is None:
			parentmenu=self['menubar'];
			
		#classmenu=self['Libclassmenu'];
		#classmenu=parentmenu;
		#classname=typestr(self).title();
		#classname=menugroupelabel;
		children=parentmenu.winfo_children();
		try:
			thismenu=self['classmenu'+menugroupelabel];
			new=0;
		except:
			thismenu = Tkinter.Menu(parentmenu, tearoff=0);
			self['classmenu'+menugroupelabel]=thismenu;
			new=1;
		if menulabel is None:
			#print "adding separator"
			thismenu.add_separator();
		else:
			#print "adding command.",menucommandfunc
			thismenu.add_command(label=menulabel, command=menucommandfunc);
			if new==1:
				parentmenu.add_cascade(label=menugroupelabel, menu=thismenu)
		return thismenu;

		
	def data_menu(self,parentmenu=None,menulabel=None):
		if parentmenu is None:
			parentmenu=self['menubar'];
			thismenu=DataMenu(parentmenu);
			parentmenu.add_cascade(label=menulabel,menu=thismenu);
		else:	
			thismenu=parentmenu.add_submenu(menulabel);
		print "menulabel",menulabel
		return thismenu;
		
	def	menu(self,menulabel):
		parentmenu=self['menubar'];
		thismenu=Menu(parentmenu,tearoff=0);
		parentmenu.add_cascade(label=menulabel,menu=thismenu);
		return thismenu;
		

	def uiquit(self):
		import tkMessageBox
		if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
			self.gcdestroy();
		
		
	def uisetnum(self):
		self.uiset(datatype='numeric');
		
	def uisetstr(self):
		self.uiset(datatype='string');
	
	def uitextout(self,pagename="Textout"):
		import textoutframe;
		mainframe=self['mainframe'];
		#frames=mainframe['screenlist'];
		foundframe=False;
		#for f in frames:
			#print f
		#	if isa(f,'TextOutFrame','textoutframe'):
		#		foundframe=True;
		pagenames=mainframe.pagenames();
		if pagenames.count(pagename)>0:
			foundframe=True;
		#print "foundframe",foundframe
		if not foundframe:
			page=mainframe.add(pagename);
			lframe=textoutframe.TextOutFrame(page,pagename);
			lframe.refresh();
			#mainframe.add_screen(lframe,'Textout');
			lframe.pack(fill=BOTH,expand=1);
			mainframe.setnaturalsize();
			mainframe.setnaturalsize();
			#lframe.pack(fill = 'both', expand = 1);
			#mainframe.setactive(-1);
			self['stdout']=lframe;
			
	def dispkeys(self):
		print self.keys();
	
	def uiexploredata(self,data2explore=None,dataname="/"):
		#print "uiexploredata"
		tpdict=self['dataexplorerframeclass'];
		modulename=tpdict['modulename'];
		typename=tpdict['typename'];
		cmd='import '+modulename;
		exec(cmd);
		exploreframe=self.getdataexplorer();
		mainframe=self['mainframe'];
		
		#print 'dataexplorer',type(dataexplorer)
		if exploreframe is None:
			page=mainframe.add('DataExplorer');
			cmd='exploreframe='+modulename+'.'+typename+"(page,self['winname'])";
			#print cmd;
			exec(cmd);
			exploreframe.pack(fill='both',expand=1);
			mainframe.setnaturalsize();
			if data2explore is None:
				data2explore=self;
			exploreframe.exploredata(data2explore,dataname);
			#mainframe.add_screen(exploreframe,'DataExplorer');
			
		#print "setactive"
			#mainframe.setactive(-1);
		#explorewin.wintitle(self['guiroot'].title());
		#print "to return",type(exploreframe)
		return exploreframe;
		
	def getdataexplorer(self):
		"""
		dataexplorer=None;
		tpdict=self['dataexplorerframeclass'];
		modulename=tpdict['modulename'];
		typename=tpdict['typename'];
		cmd='import '+modulename;
		exec(cmd);
		
		mainframe=self['mainframe'];
		pagenames=mainframe.pagenames();
		if pagenames.count("DataExplorer")>0:
#			page=mainframe.page("DataExplorer");
			page=mainframe.page("DataExplorer");
			dataexplorer=page.winfo_children()[0];
		#frames=mainframe['screenlist'];
		#for f in frames:
			#print f
		#	if isa(f,typename,modulename):
		#		dataexplorer=f;
		#print "in get dataexplorer",type(dataexplorer)	
		"""
		dataexplorer=self.findframeinnotebook("DataExplorer");
		return dataexplorer;
		
	def uiexit(self):
		guiroot=self['guiroot'];
		guiroot.destroy();
		
	def getrootdatawin(self):
		winchain=self.getdatawinchainobj();
		return winchain[0];
		
	def getparentdatawin(self):
		import datatkwindow as dw;
		parentdatawin=None;
		winchain=self.getdatawinchainobj();
		if len(winchain)>1:
			parentdatawin=winchain[-2];
			if not isinstance(parentdatawin,dict):
				parentdatawin=dw.DataTkWindow(tkwin=parentdatawin);
				parentdatawin=dw.DataTkWindow(tkwin=parentdatawin);	
		return parentdatawin;
		
	def getdatawinchainname(self):
		winchain=self.getdatawinchainobj();
		namechain=[];
		for i in winchain:
			namechain.append(i['winname']);
		return namechain
	
	def getdatawinchainclass(self):
		winchain=self.getdatawinchainobj();
		classchain=[];
		for i in winchain:
			classchain.append(typestr(i));
		return classchain;
		
	def getdatawinchainstr(self):
		winchain=self.getdatawinchainobj();
		strchain='';
		#print "getdatawinchainstr"
		for i in winchain:
			#print type(i), i['winname']
			strchain=strchain+'/'+i['winname']+'<'+typestr(i)+'>';
		return strchain

	def getdatawinpathstr(self):
		winpath=self.getdatawinchainobj();
		winpath.pop();
		strpath='';
		#print "getdatawinpathstr"
		for i in winpath:
			#print type(i), i['winname']
			strpath=strpath+'/'+i['winname']+'<'+typestr(i)+'>';
		if strpath=='':
			strpath='/';
		return strpath
		
	def getdatawinchainobj(self):
		winchain=[self];
		datawin=self;
		parentdatawin=self['guiroot'].master;
		#raw_input()
		
		#print "getdatawinchainobj"
		#print type(parentdatawin),type(datawin)
		#print "isinstance(parentdatawin,dict)", isinstance(parentdatawin,dict)
		while isinstance(parentdatawin,dict):
			winchain.insert(0,parentdatawin);
			datawin=parentdatawin;
			parentdatawin=datawin.getmaster();
			#print type(parentdatawin),type(datawin)
		return winchain;
		
	def loadimage(self,imagefilename):
		import os;
		from PIL import Image, ImageTk;
		rootwin=self.getrootdatawin();
		imagedir=rootwin['imagedir'];
		rootdir=rootwin['approotdir'];
		#curdir= os.path.abspath(os.curdir)
		imagefile=os.path.join(rootdir,imagedir);
		imagefile=os.path.join(imagefile,imagefilename);
		#print imagefile
		image = Image.open(imagefile);
		imageobj = ImageTk.PhotoImage(image);
		return imageobj;
		
	def getextensionwin(self):
		extwin=None;
		import extensionwin;
		children=self['guiroot'].winfo_children();
		for c in children:
			if isa(c,'ExtensionWin','extensionwin'):
				extwin=c;
		if extwin is None:
			extwin=extensionwin.ExtensionWin(self);
		return extwin;	
	
	def getposition(self):
		import re;
		posstr=self['guiroot'].geometry();
		#print "posstr",posstr
		#g=re.search("(\d+)x(\d+)\+(\d+)\+(\d+)",posstr);
		g=re.search("(\d+)x(\d+)([-+]\d+)([-+]\d+)",posstr);
		pos={};
		pos['dx']=int(g.group(1));
		pos['dy']=int(g.group(2));
		pos['x0']=int(g.group(3));
		pos['y0']=int(g.group(4));
		#print "pos",pos
		return pos;
		
	def setposition(self,x0=None,y0=None,dx=None,dy=None):
		pos=self.getposition();
		#print "pos",pos
		if x0 is not None and y0 is not None:
			pos['x0']=x0;
			pos['y0']=y0;
			posstr='+'+str(pos['x0'])+'+'+str(pos['y0']);
			self['guiroot'].geometry(posstr);
		if dx is not None and dy is not None:
			pos['dx']=dx;
			pos['dy']=dy;
			posstr=	str(pos['dx'])+'x'+str(pos['dy']);
			self['guiroot'].geometry(posstr);
		#print "posstr",posstr
	
	def shiftposition(self,xshift=0,yshift=0):
		pos=self.getposition();
		x0=pos['x0']+xshift;
		y0=pos['y0']+yshift;
		#self.stdout((x0,y0,pos['dx'],pos['dy']));
		self.setposition(x0,y0);
		
	def getmaster(self):
		return self['guiroot'].master;
		
	def gcdestroy(self):
		guiroot=self['guiroot'];
		self.cleardata();
		guiroot.destroy();
		
	def addpage(self,framename):
		mainframe=self['mainframe'];
		page=mainframe.add(framename);
		return page;
		
	def findframeinnotebook(self,framename):
		frame=None;
		mainframe=self['mainframe'];
		pagenames=mainframe.pagenames();
		#print "pagenames",mainframe.pagenames()
		if pagenames.count(framename)>0:
			page=mainframe.page(framename);
			frame=page.winfo_children()[0];
		return frame;
	
	def findchildwin(self,winname):
		childwinfound=None;
		for c in self.winfo_children():
			if isinstance(c,Tkinter.Toplevel):
				try:
					if winname==c['winname']:
						childwinfound=c;
				except:
					self.stdout("Found non-data toplevel");
		return childwinfound;
		
	def getchildwinlist(self):
		childwinlist=[];
		for c in self.winfo_children():
			if isinstance(c,Tkinter.Toplevel) and isdatobj(c):
				childwinlist.append(c);
		return childwinlist;

	def getsubwinlist(self):
		childwinlist=self.getchildwinlist();
		subwinlist=childwinlist;
		for c in childwinlist:
			childwinlist=c.getsubwinlist();
			subwinlist=subwinlist+childwinlist;
		return subwinlist;