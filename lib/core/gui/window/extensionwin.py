from datatoplevelwindow import *; 

class ExtensionWin(DataToplevelWindow):
	def __init__(self,parentdatawin):
		DataToplevelWindow.__dict__['__init__'](self,parentdatawin);
		self['winname']=parentdatawin['winname']+'.Toolbox';
		self.__ginit();
		
	def __ginit(self):
		self.wintitle();