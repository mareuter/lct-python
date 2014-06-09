# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2012-2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

from PyQt4 import QtCore
from PyQt4 import QtGui

from .ui_location_config import Ui_LocationConfigDialog
from lct.utils.observing_info import ObservingInfo

class LocationConfig(QtGui.QDialog, Ui_LocationConfigDialog):
    '''
    This dialog is for setting the latitude and longitude for an observing 
    location.
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(LocationConfig, self).__init__(parent)
        self.setupUi(self)
        
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        
        # Validator for latitude degrees
        latdegval = QtGui.QIntValidator()
        latdegval.setRange(0, 90)
        # Validator for longitude degrees
        longdegval = QtGui.QIntValidator()
        longdegval.setRange(0, 180)
        # Validator for minutes/seconds
        hexval = QtGui.QIntValidator()
        hexval.setRange(0, 60)
        
        self.lat_deg_edit.setValidator(latdegval)
        self.lat_min_edit.setValidator(hexval)
        self.lat_sec_edit.setValidator(hexval)
        
        self.long_deg_edit.setValidator(longdegval)
        self.long_min_edit.setValidator(hexval)
        self.long_sec_edit.setValidator(hexval)
        
        # Setup the checks for valid lineedit content
        self.connect(self.loc_edit, QtCore.SIGNAL("editingFinished()"), 
                     self._checkLineEdits)
        self.connect(self.lat_deg_edit, QtCore.SIGNAL("editingFinished()"), 
                     self._checkLineEdits)
        self.connect(self.lat_min_edit, QtCore.SIGNAL("editingFinished()"), 
                     self._checkLineEdits)
        self.connect(self.lat_sec_edit, QtCore.SIGNAL("editingFinished()"), 
                     self._checkLineEdits)
        self.connect(self.long_deg_edit, QtCore.SIGNAL("editingFinished()"), 
                     self._checkLineEdits)
        self.connect(self.long_min_edit, QtCore.SIGNAL("editingFinished()"), 
                     self._checkLineEdits)
        self.connect(self.long_sec_edit, QtCore.SIGNAL("editingFinished()"), 
                     self._checkLineEdits)

    def _checkLineEdits(self):
        '''
        This function checks the lineedits to make sure that all of them 
        have valid information before allowing the Ok button to be enabled.
        '''
        lineedits = (self.loc_edit, self.lat_deg_edit, self.lat_min_edit,
                     self.lat_sec_edit, self.long_deg_edit, self.long_min_edit,
                     self.long_sec_edit)
        for lineedit in lineedits:
            if lineedit.text().isEmpty():
                return
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        
    def setLocation(self):
        '''
        This function gathers the information recorded in the dialog and 
        transfers it to the observation site object.
        '''
        obs_info = ObservingInfo()
        lat_deg = self.lat_deg_edit.text().toInt()[0]
        lat_min = self.lat_min_edit.text().toInt()[0]
        lat_sec = self.lat_sec_edit.text().toInt()[0]
        lat_dir = self.lat_dir_cb.currentText()
        if lat_dir == 'S':
            lat_deg *= -1
    
        long_deg = self.long_deg_edit.text().toInt()[0]
        long_min = self.long_min_edit.text().toInt()[0]
        long_sec = self.long_sec_edit.text().toInt()[0]
        long_dir = self.long_dir_cb.currentText()
        if long_dir == 'W':
            long_deg *= -1
        
        obs_info.obs_site.setLocationName(self.loc_edit.text())
        obs_info.obs_site.fromCoordTuple('lat', (lat_deg, lat_min, lat_sec))
        obs_info.obs_site.fromCoordTuple('long', (long_deg, long_min, long_sec))
        self.emit(QtCore.SIGNAL("updateLocation"))
        