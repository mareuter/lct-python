# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2012-2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

from PyQt4 import QtCore
from PyQt4 import QtGui

import lct.ui.ui_mainwindow as um
import lct.ui.widgets as uw
import lct.utils.observing_info as oi
from . import version

class LunarClubTools(QtGui.QMainWindow, um.Ui_MainWindow):
    '''
    This is the main class for the program.
    '''
    
    def __init__(self, datetimestr=None, parent=None):
        '''
        Constructor
        @param datetimestr: A string containing a date/time representation.
        '''
        super(LunarClubTools, self).__init__(parent)
        import logging
        self.logger = logging.getLogger('lct.utils.main_window.LunarClubTools')
        
        self.setupUi(self)
        self.logger.debug("Main program UI setup.")
        self.tabWidget.setCurrentIndex(0)
        
        self.connect(self.actionExit, QtCore.SIGNAL("triggered()"),
                     self.close)
        self.connect(self.actionLocation, QtCore.SIGNAL("triggered()"),
                     self.openLocationConfigDialog)
        self.connect(self.actionLunarClubTools, QtCore.SIGNAL("triggered()"),
                     self.about)
        
        self.updateTime(datetimestr)
        self.logger.debug("Date/time updated.")
        self.updateUI()
        self.logger.debug("Widget UIs updated.")
        
    def updateUI(self):
        '''
        This function updates the main window UI and the sub-component UIs.
        '''
        self.logger.debug("Starting LunarClubTools::updateUI.")
        self.moonInfoTab.updateUI()
        self.logger.debug("MoonInfoTab UI updated.")
        self.lunarClubTab.updateUI()
        self.logger.debug("LunarClubTab UI updated.")
        self.lunarTwoTab.updateUI()
        self.logger.debug("LunarTwoTab UI updated.")
        
    def updateTime(self, datetimestr):
        '''
        This function updates the time in the ObservingInfo object and calls its 
        update function.
        @param datetimestr: A string containing a date/time representation.
        '''
        self.logger.debug("Starting LunarClubTools::updateTime.")
        obsinfo = oi.ObservingInfo()
        obsinfo.obs_site.setDateTime(datetimestr)
        obsinfo.update()
        
    def closeEvent(self, event):
        '''
        This function handles issues that need to be addressed when the 
        program closes.
        @param event: The current event.
        '''
        pass
        
    def openLocationConfigDialog(self):
        '''
        This function sets up and opens the location configuration dialog.
        '''
        dialog = uw.location_config.LocationConfig()
        self.connect(dialog, QtCore.SIGNAL("updateLocation"), self.updateUI)
        if dialog.exec_():
            dialog.setLocation()
           
    def about(self):
        '''
        This function creates the about dialog box.
        '''
        QtGui.QMessageBox.about(self, "About Lunar Club Tools",
                                """
                                <b>Lunar Club Tools</b> v%s
                                <p>This application determines the current 
                                features visible for the Astronomical League's 
                                Lunar Club and Lunar II Club.
                                <br><br>
                                Copyleft 2012 Type II Software
                                """ % version.version)
    