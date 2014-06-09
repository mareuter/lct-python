# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

from PyQt4 import QtGui

from .ui_lunar_club_special_widget import Ui_LunarClubSpecialWidget
from lct.utils.observing_info import ObservingInfo
from lct.utils.string_format import StrFmt
import lct.utils.constants as constants
from . import widget_resources_rc

class LunarClubSpecialWidget(QtGui.QWidget, Ui_LunarClubSpecialWidget):
    '''
    This class is responsible for displaying information for the special categories of the 
    Lunar Club list.
    '''
    
    # The maximum number of hours to/from new Moon for observations.
    TIME_CUTOFF = 72.0
    # The maximum number of hours for the age of the waxing crescent.
    TIME_WAXING_CRESENT = 40.0
    # The maximum number of hours for the age of the waning crescent.
    TIME_WANING_CRESENT = 48.0
    # Time range in days for the Cow Jumping over the Moon observation.
    TIME_COW_JUMPING = [2.0, 3.0]
    # Illuminated fraction for Full Moon.
    FULL_MOON_FRACTION = 0.987
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(LunarClubSpecialWidget, self).__init__(parent)
        self.setupUi(self)
        self._star_on = ":/star-on.svg"
        self._set_css_labels(self.time_from_new_moon_label, self.time_from_new_moon_time_label,
                             self.old_moon_in_new_moon_arms_label,
                             self.cresent_moon_waxing_label,
                             self.time_to_new_moon_label, self.time_to_new_moon_time_label,
                             self.new_moon_in_old_moon_arms_label,
                             self.cresent_moon_waning_label,
                             self.cow_jumping_over_moon_label,
                             self.man_in_the_moon_label,
                             self.woman_in_the_moon_label,
                             self.rabbit_in_the_moon_label)

    def updateUI(self):
        '''
        This function is for handling things that need to be updated on the UI.
        '''
        obsinfo = ObservingInfo()
        obsinfo.update()
        
        # Time from new moon calculations
        hrs_from_new = obsinfo.moon_info.timeFromNewMoon()
        if hrs_from_new <= LunarClubSpecialWidget.TIME_CUTOFF:
            self.time_from_new_moon_time_label.setText(StrFmt.floatString(hrs_from_new, 
                                                                          1, " hours"))
           
            if hrs_from_new > LunarClubSpecialWidget.TIME_WAXING_CRESENT:
                self.old_moon_in_new_moon_arms_indicator.setPixmap(QtGui.QPixmap(self._star_on))
            else:
                self.cresent_moon_waxing_indicator.setPixmap(QtGui.QPixmap(self._star_on))
                
        # Time to new moon calculations
        hrs_to_new = obsinfo.moon_info.timeToNewMoon()
        if hrs_to_new <= LunarClubSpecialWidget.TIME_CUTOFF:
            self.time_to_new_moon_time_label.setText(StrFmt.floatString(hrs_to_new, 
                                                                        1, " hours"))
            
            if hrs_to_new > LunarClubSpecialWidget.TIME_WANING_CRESENT:
                self.new_moon_in_old_moon_arms_indicator.setPixmap(QtGui.QPixmap(self._star_on))
            else:
                self.cresent_moon_waning_indicator.setPixmap(QtGui.QPixmap(self._star_on))
        
        # Time to full moon calculation, only needed for Cow Jumping over the Moon.   
        days_to_full = obsinfo.moon_info.timeToFullMoon()
        if days_to_full >= LunarClubSpecialWidget.TIME_COW_JUMPING[0] and \
            days_to_full <= LunarClubSpecialWidget.TIME_COW_JUMPING[1]:
            self.cow_jumping_over_moon_indicator.setPixmap(QtGui.QPixmap(self._star_on))
            
        # All other <Blank> in the Moon will use the illuminated fraction
        illum = float(obsinfo.moon_info.illumination()) * 0.01
        if illum >= LunarClubSpecialWidget.FULL_MOON_FRACTION:
            self.man_in_the_moon_indicator.setPixmap(QtGui.QPixmap(self._star_on))
            self.woman_in_the_moon_indicator.setPixmap(QtGui.QPixmap(self._star_on))
            self.rabbit_in_the_moon_indicator.setPixmap(QtGui.QPixmap(self._star_on))
                    
    def _set_css_labels(self, *args):
        '''
        This function sets the stylesheets for the labels.
        @param args: The set of QLabels to be styled. 
        '''
        for arg in args:
            arg.setStyleSheet(constants.CSS_MOON_INFO_EDITS)