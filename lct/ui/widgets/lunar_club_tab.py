'''
Created on Jun 9, 2012

@author: Michael Reuter
'''
from PyQt4 import QtGui, QtCore
from ui_lunar_club_tab import Ui_LunarClubTabWidget
import features
import utils

class LunarClubTab(QtGui.QWidget, Ui_LunarClubTabWidget):
    '''
    This class is responsible for listing the features visible for the Lunar 
    Club target list.
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(LunarClubTab, self).__init__(parent)
        self.setupUi(self)
        self.features = features.LunarFeatureContainer()
        
    def updateUI(self):
        '''
        This function is for handling things that need to be updated on the 
        UI.
        '''
        self.features.load()
        self.populateLunarClubTree()
        
    def populateLunarClubTree(self):
        '''
        This function populates the features from the Lunar Club into the 
        corresponding tree.
        '''
        self.lunar_club_tree.clear()
        self.lunar_club_tree.setColumnCount(2)
        self.lunar_club_tree.setHeaderLabels(["Target/Type/Name", "Latitude"])
        self.lunar_club_tree.setItemsExpandable(True)
        parentFromTarget = {}
        # Set Target values first since they need to be in a specific order.
        for club_type in utils.LUNAR_CLUB_TARGET_TYPES:
            # Need to be QStrings to match object in LunarFeature
            qstr_club_type = QtCore.QString(club_type)
            ancestor = QtGui.QTreeWidgetItem(self.lunar_club_tree, 
                                             [qstr_club_type])
            parentFromTarget[qstr_club_type] = ancestor
        
        parentFromType = {}
        for feature in self.features.inOrder():
            if feature.code_name in ("Lunar", "Both"):
                ancestor = parentFromTarget.get(feature.club_type) 
                targettype = feature.club_type + "/" + feature.feature_type
                parent = parentFromType.get(targettype)
                if parent is None:
                    parent = QtGui.QTreeWidgetItem(ancestor, 
                                                       [feature.feature_type])
                    parentFromType[targettype] = parent
                feature_lat_str = utils.StrFmt.ddString(feature.latitude, 2, 
                                                        "latitude")
                item = QtGui.QTreeWidgetItem(parent, [feature.name,
                                                      QtCore.QString("%1").arg(feature_lat_str)])
                item.setTextAlignment(1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.lunar_club_tree.expandItem(parent)
                self.lunar_club_tree.expandItem(ancestor)
        self.lunar_club_tree.resizeColumnToContents(0)
        self.lunar_club_tree.resizeColumnToContents(1)
