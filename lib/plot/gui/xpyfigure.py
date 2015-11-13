from dataexplorerwin import *;
from datatkwindow import *;
from Tkinter import *;
import pylab;
import easygui;

class XpyFigure(DataTkWindow):
	def __init__(self,fignum=None,approotwin=None):
		needginit=self.pyfiginit(fignum,approotwin);
		tkwin=self.gettkwin()
		DataTkWindow.__dict__['__init__'](self,winname=tkwin.title(),tkwin=tkwin);
		if needginit:
			self.ginit();
			
	def pyfiginit(self,fignum=None,approotwin=None):
		needginit=False;
		if fignum is None:
			pyfig=pylab.figure();
			self['pyfig']=pyfig;
			pyfig.userdata={};
			if approotwin is not None:
				pyfig.userdata['approotwin']=approotwin;
			needginit=True;
		else:
			pyfig=pylab.figure(fignum);
			self['pyfig']=pyfig;
			if not hasattr(pyfig,'userdata'):
				pyfig.userdata={};
				if approotwin is None:
					#print "need approotwin!"
					pass;
				else:
					pyfig.userdata['approotwin']=approotwin;
				needginit=True;
		return needginit;
	
	def ginit(self):
		tkwin=self.gettkwin();
		tkwin.protocol("WM_DELETE_WINDOW", self.uiquit)
		self.menus();
		
	def menus(self):
		tkwin=self.gettkwin();
		menubar=Menu(tkwin);
		tkwin.configure(menu=menubar);
		
		figmenu=Menu(menubar,tearoff=0);
		menubar.add_cascade(label="Figure",menu=figmenu);
		figmenu.add_command(label="Grid",command=self.grid);

		figmenu=Menu(menubar,tearoff=0);
		menubar.add_cascade(label="Line",menu=figmenu);
		figmenu.add_command(label="Convert unit",command=self.convertxunit);
		
		tkwin.bind("<Button-3>", lambda event:self.rightclick(event));
		tkwin.bind("<Button-1>", lambda event:self.leftclick(event));
		
	def rightclick(self,event):
		#print "even button",event.button
		menu=self.contextmenu();
		#print event.x,event.y;
		menu.post(event.x_root, event.y_root)
	
	def leftclick(self,event):
		self.setcurrent();

	def contextmenu(self):
		tkwin=self.gettkwin();
		menu=Menu(tkwin,tearoff=0);
		
		# grid and hold
		menu.add_command(label="Grid",command=self.grid);
		if self.ishold():
			holdlabel="Hold is on, click to toggle";
		else:
			holdlabel="Hold is off, click to toggle";
		menu.add_command(label=holdlabel,command=lambda:self.hold());
		
		#axes
		axismenu=Menu(menu,tearoff=0);
		menu.add_cascade(label="Axis",menu=axismenu);
		axismenu.add_command(label='Tight',command=self.axistight);
		axismenu.add_command(label="Set",command=self.axissetlimit);
		axismenu.add_command(label="x 2",command=lambda:self.axiszoom(2));
		axismenu.add_command(label="linear x scale",command=lambda:self.setxscale("linear"));
		axismenu.add_command(label="logrithmic x scale",command=lambda:self.setxscale("log"));
		axismenu.add_command(label="linear y scale",command=lambda:self.setyscale("linear"));
		axismenu.add_command(label="logrithmic y scale",command=lambda:self.setyscale("log"));
		#for lines
		linemenu=Menu(menu,tearoff=0);
		menu.add_cascade(label="Line",menu=linemenu);
		linemenu.add_command(label='Set width',command=self.setalllinewidth);
		
		#for legend
		menu.add_command(label="Legend",command=self.uisetlegend);
		
		menu.add_separator();
		# for xyplotable object
		menu.add_command(label="Convertxunits",command=self.convertxunit);
		menu.add_command(label="Explore",command=self.exploredata);
		menu.add_command(label="Refresh",command=self.refresh);
		
		return menu;
		
	def grid(self):
		self.setcurrent();
		pylab.grid();
	
	def hold(self,onoff=None):
		self.setcurrent();
		pylab.hold(onoff);
	
	def ishold(self):
		self.setcurrent();
		return pylab.gca().ishold();
	
	def setcurrent(self):
		pyfig=self['pyfig'];
		fignum=pyfig.number;
		pylab.figure(fignum);
	
	def convertxunit(self):
		pyfig=self['pyfig']
		newlines=pyfig.userdata['linetable'].copy();
		i=0;
		xunitnew=None;
		for k in newlines.keys():
			line=newlines[k];
			if i==0:
				xunit=line['xunit'];
				xunitnames=xunit['dict'].keys();
				#currentunit=xunit["currentunit"];
				#I=xunitnames.index(currentunit);
				#xunitnames.pop(I);
				xunitnew=easygui.choicebox("choose a new xunit","converting x unit",xunitnames);
			i=i+1;	
			if xunitnew is not None:
				line.convertx(xunitnew);
		if xunitnew is not None:
			xfig=XpyFigure();
			newlines.plot();
			if pyfig.userdata.has_key('legendfieldname'):
				legendfieldname=pyfig.userdata['legendfieldname'];
				xfig.setlegend(legendfieldname);
		#pyfig.userdata['linetable']=newlines;
		#pass;
		
	def uisetlegend(self):
		pyfig=self['pyfig']
		lines=pyfig.userdata['linetable'];
		keys=lines.keys();
		fieldnames=lines.fullcolumnlist();
		line0=lines[keys[0]];
		fieldnames0=fieldnames[:];
		for fname in fieldnames0:
			v=line0.get(fname);
			#print "v type:",type(v)
			if not isstring(v) and not isnumeric(v) and v is  not None:
				#print "non-legend",fname,":",type(v);
				I=fieldnames.index(fname);
				fieldnames.pop(I);
			#else:
			#	print "legend",fname,":",type(v);
				
		legendfieldname=easygui.choicebox("choose a field","Setting legend",fieldnames);
		
		if legendfieldname is not None:
			self.setlegend(legendfieldname,lines);
		
	def setlegend(self,legendfieldname,lines=None):
		if lines is None:
			pyfig=self['pyfig']
			lines=pyfig.userdata['linetable'];
			
		valuelist=lines.aggselect(legendfieldname);
		seqkeys=lines.seqkeys();
		keys=lines.keys();
		legendstrlist=[];
		for k in seqkeys:
			I=keys.index(k);
			v=valuelist[I];
	#		for v in valuelist:
			legendstrlist.append(str(v));
		pylab.legend(tuple(legendstrlist))
		pyfig=self['pyfig'].userdata['legendfieldname']=legendfieldname;
		
	def exploredata(self):
		pyfig=self['pyfig'];
		s="Figure "+str(pyfig.number);
		tkwin=self.gettkwin();
		#dtkwin=DataTkWindow(tkwin=tkwin);
		ewin=DataExplorerWin(self,s);
		ewin.explore(pyfig.userdata,s);
		
	def axistight(self):
		self.setcurrent();
		pylab.axis('tight');
		
	def axissetlimit(self):
		self.setcurrent();
		A=pylab.axis();
		Astr=easygui.enterbox("enter the limit","axis set limit",str(A));
		if Astr is not None:
			pylab.axis(eval(Astr));
			
	def axiszoom(self,nzoom):
		self.setcurrent();
		A=pylab.axis();
		alist=list(A);
		alist[0]=A[0]-(A[1]-A[0])*(nzoom-1)/2;
		alist[1]=A[1]+(A[1]-A[0])*(nzoom-1)/2;
		alist[2]=A[2]-(A[3]-A[2])*(nzoom-1)/2;
		alist[3]=A[3]+(A[3]-A[2])*(nzoom-1)/2;
		pylab.axis(tuple(alist));
		
	def setxscale(self,scale):
		self.setcurrent();
		pylab.gca().set(xscale=scale);

	def setyscale(self,scale):
		self.setcurrent();
		pylab.gca().set(yscale=scale);
		
	def setalllinewidth(self):
		answer=easygui.enterbox("Line width?","Setting line width","2");
		if answer is not None:
			lw=int(answer);
			self.setcurrent();
			lines=pylab.gca().lines;
			for l in lines:
				l.set(linewidth=lw);
	
	def gettkwin(self):
		import time;
#		t=time.time();
		if self.has_key('tkwin'):
			tkwin=self['tkwin'];
		else:
			self.setcurrent();
			winman=pylab.get_current_fig_manager();
			tkwin=winman.window;
			self['tkwin']=tkwin;
#		print time.time()-t
		return tkwin;
		
	def add_plotable(self,xyfun,name=None):
		import plotabledataobjtable;
		pyfig=self['pyfig']
		#print "tkwin",tkwin
		if not pyfig.userdata.has_key('linetable'):
			pyfig.userdata['linetable']=plotabledataobjtable.PlotableDataObjTable();
		pyfig.userdata['linetable'].insert(xyfun,name);

	def getmaster(self):
		pyfig=self['pyfig'];
		if pyfig.userdata.has_key('approotwin'):
			master=pyfig.userdata['approotwin'];
		else:
			master=DataTkWindow.getmaster(self);
		return master;

	def gcdestroy(self):
		pyfig=self['pyfig'];
		for k in pyfig.userdata.keys():
			del pyfig.userdata[k];
		DataWindow.__dict__['gcdestroy'](self);
		
	def refresh(self):
		hold=self.ishold();
		self.hold(False);
		pyfig=self['pyfig'];
		pyfig.userdata['linetable'].plot();
		self.hold(hold);