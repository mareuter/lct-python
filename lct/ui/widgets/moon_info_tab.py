'''
Created on Jun 1, 2012

@author: Michael Reuter
'''
from PyQt4 import QtGui

from .ui_moon_info_tab import Ui_MoonInfoTabWidget
from lct.utils.observing_info import ObservingInfo
from lct.utils.string_format import StrFmt
import lct.utils.constants as constants

class MoonInfoTab(QtGui.QWidget, Ui_MoonInfoTabWidget):
    '''
    This class handles displaying common information about the Moon.
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(MoonInfoTab, self).__init__(parent)
        self.setupUi(self)
        self._set_css_labels(self.last_obs_label, self.local_date_label, self.utc_date_label,
                             self.location_label, self.moon_age_label,
                             self.moon_colong_label, self.moon_illum_label,
                             self.moon_phase_label, self.moon_libration_lat_label,
                             self.moon_libration_long_label)
        self._set_css_edits(self.local_date_edit, self.utc_date_edit,
                            self.location_edit, self.moon_age_edit, self.moon_age_units_label,
                            self.moon_colong_edit, self.moon_illum_edit,
                            self.moon_phase_edit, self.moon_libration_lat_edit,
                            self.moon_libration_long_edit)
        
    def updateUI(self):
        '''
        This function is responsible for updating the GUI widgets with the 
        current Moon information from the current observation time.
        '''
        obsinfo = ObservingInfo()
        obsinfo.update()

        tz_fmt = " (" + obsinfo.obs_site.getLocalTimezone() + "):"
        self.local_date_label.setText(self.local_date_label.text() + tz_fmt)
        self.local_date_edit.setText(obsinfo.obs_site.getLocalDate())
        self.utc_date_edit.setText(obsinfo.obs_site.getUtcDate())
        
        self.moon_phase_edit.setText(obsinfo.moon_info.getPhaseAsString())
        self.moon_illum_edit.setText(obsinfo.moon_info.illumination(True))
        self.moon_colong_edit.setText(StrFmt.dmsString(obsinfo.moon_info.colong().split(':')))
        self.moon_age_edit.setText(obsinfo.moon_info.age())
        self.moon_libration_lat_edit.setText(obsinfo.moon_info.libration('lat'))
        self.moon_libration_long_edit.setText(obsinfo.moon_info.libration('long'))
        
        self.location_edit.setText(obsinfo.obs_site.getLocationString())
        
    def _set_css_labels(self, *args):
        '''
        This function sets the stylesheets for the labels.
        @param args: The set of QLabels to be styled. 
        '''
        for arg in args:
            arg.setStyleSheet(constants.CSS_MOON_INFO_LABELS)
        
    def _set_css_edits(self, *args):
        '''
        This function sets the stylesheets for the "lineedits".
        @param args: The set of QLabels to be styled. 
        '''
        for arg in args:
            arg.setStyleSheet(constants.CSS_MOON_INFO_EDITS)
            
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    widget = MoonInfoTab()
    widget.move(0, 0)
    widget.show()
    widget.updateUI()
    #widget.resize(400, 400)
    app.exec_()
