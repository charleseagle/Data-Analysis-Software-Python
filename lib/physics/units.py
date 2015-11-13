from dataobject import *;

class Units(DataObject):
	def __init__(self):
		self['dict']={'unitname':'varname'};
		self['tolerancedict']={'unitname':1e-10};
		self['defaultunit']="unitname";
		self['currentunit']="unitname";
		
	def convertfromto(self,x,fromunit,tounit):
		#print "=========in convertxunit========"
		#print " fromunit",fromunit,"tounit",tounit
		if self['dict'].has_key(fromunit) and self['dict'].has_key(tounit):
			if fromunit==self['currentunit']:
				cmd='xnew=self.'+fromunit+'2'+tounit+'(x)';
				exec(cmd);
				self['currentunit']=tounit;
				return xnew
			else:
				print fromunit,'does not match',self['xcurrentunit']
		else:
			print fromunit,tounit,"wrong unit."
			
	def convert(self,x,tounit):
		xnew=x;
		if self['currentunit']!=self['defaultunit']:
			#print "===========in convertx=========="
			xnew=self.convertfromto(x,self['currentunit'],self['defaultunit']);
		if 	self['defaultunit']!=tounit:
			xnew=self.convertfromto(xnew,self['defaultunit'],tounit);
		return xnew;
		
	def setcurrentunit(self,unitname="unitname",varname=None):
		self['currentunit']=unitname;
		if varname is not None:
			self.addunit(unitname,varname);
		#if not self['dict'].has_key(unitname):
		#	self.addunit(varname,unitname);
	
	"""
	def setcurrentvar(self,varname,unitname='unitname'):
		foundvarname=False;
		for k in self['dict'].keys():
			if self['dict'][k]==varname:
				self.setcurrentunit(k);
				foundvarname=True;
		if not foundvarname:
			self['dict'][unitname]=varname;
			self['currentunitname']='unitname';
	"""
	
	def addunit(self,unitname='unitname',varname="varname"):
		self['dict'][unitname]=varname;
	
	def getcurrentunit(self):
		return self['currentunit'];
		
	def getcurrentvar(self):
		unitname=self['currentunit'];
		return self['dict'][unitname];
		
	def getcurrenttolerance(self):
		unitname=self['currentunit'];
		return self['tolerancedict'][unitname];
		
	def uisetcurrentunit(self):
		import easygui;
		currentvalues=[self.getcurrentvar(),self.getcurrentunit()];
		answer=easygui.multenterbox("Enter the unit info","Setting units",['Variable name','Unit name'],currentvalues);
		if answer is not None:
			self.setcurrentunit(answer[1],answer[0]);
			
	def contextmenu(self,menu,dataname=None):
		menu=DataObject.contextmenu(self,menu);
		menu.add_separator();
		topwin=menu.gettoplevel();
		menu.add_command(label="Set unit",command=lambda:self.uisetcurrentunit());
		return menu;