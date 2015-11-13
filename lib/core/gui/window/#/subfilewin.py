from savablewin import *; 

class SubFileWin(SavableWin):
	def __init__(self,parentdatawin=None,winname='unnamed'):
		SavableWin.__dict__['__init__'](self,parentdatawin,winname);
		self['savabledata']['class']=typestr(self);
		self.__ginit();
		
	def __ginit(self):
		self.addclassmenu('Subfilewin',"Save to parent file",lambda cmd='self.save':self.logrun(cmd));
		self.addclassmenu('Subfilewin',"Save to parent file as",lambda cmd='self.saveas':self.logrun(cmd));
		#self.log({'cmd':'__ginit','msg':t+' created.'});
		self.wintitle();
		return True;
				
	def save(self):
		self['parent']['savabledata']['dataofchildren'][self['winname']]=self['savabledata'];
		#print 'saving...'
		return True;
		
	def saveas(self):
		print 'saveas'
		success=False;
		winname=easygui.enterbox('Enter the name','Saving '+self['winname']+' as',self['winname']);
		if winname!=None:
			self['winname']=winname;
			self.save();
			success=True;
		return success;