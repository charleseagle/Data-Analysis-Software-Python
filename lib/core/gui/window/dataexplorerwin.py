from datatoplevelwindow import *; 
from dataexplorerframe import *;

from Tkinter import *;

class DataExplorerWin(DataToplevelWindow):
	def __init__(self,parentdatawin=None,winname='DataExplorer'):
		#self['imagedir']="image";
		DataToplevelWindow.__dict__['__init__'](self,parentdatawin,winname);
		self.__ginit();
		
	def __ginit(self):
		exploreframe=self.uiexploredata();
		self['explorerframe']=exploreframe;
		
	def explore(self,datadict,dataname="/"):
		self['explorerframe'].exploredata(datadict,dataname);