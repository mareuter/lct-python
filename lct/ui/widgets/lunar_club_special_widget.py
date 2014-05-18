'''
Created on May 18, 2014

@author: Michael Reuter
'''
from PyQt4 import QtGui

from .ui_lunar_club_special_widget import Ui_LunarClubSpecialWidget

class LunarClubSpecialWidget(QtGui.QWidget, Ui_LunarClubSpecialWidget):
    '''
    This class is responsible for displaying information for the special categories of the 
    Lunar Club list.
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(LunarClubSpecialWidget, self).__init__(parent)
        self.setupUi(self)

    def updateUI(self):
        '''
        This function is for handling things that need to be updated on the 
        UI.
        '''
        pass