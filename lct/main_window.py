'''
Created on Jun 1, 2012
@author: Michael Reuter
'''
from PyQt4 import QtCore, QtGui
import ui.widgets
import version

class LunarClubTools(QtGui.QMainWindow, ui.Ui_MainWindow):
    '''
    This is the main class for the program.
    '''
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(LunarClubTools, self).__init__(parent)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        
        self.connect(self.actionExit, QtCore.SIGNAL("triggered()"),
                     self.close)
        self.connect(self.actionLocation, QtCore.SIGNAL("triggered()"),
                     self.openLocationConfigDialog)
        self.connect(self.actionLunarClubTools, QtCore.SIGNAL("triggered()"),
                     self.about)
        
        self.updateUI()
        
    def updateUI(self):
        '''
        This function updates the main window UI and the sub-component UIs.
        '''
        self.moonInfoTab.updateUI()
        self.featuresTab.updateUI()
        
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
        dialog = ui.widgets.LocationConfig()
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
           
def main():
    '''
    This is the entrance point for the program.
    '''
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("Type II Software")
    app.setApplicationName("Lunar Club Tools")
    form = LunarClubTools()
    form.show()
    app.exec_()
    