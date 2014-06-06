# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

from PyQt4 import QtGui
from PyQt4 import QtCore

from .ui_lunar_two_tab import Ui_LunarTwoTabWidget
import lct.features.lunar_feature_container as lfc
from lct.utils.string_format import StrFmt

class LunarTwoTab(QtGui.QWidget, Ui_LunarTwoTabWidget):
    '''
    This class is responsible for listing the features visible for the Lunar II 
    club target list.
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(LunarTwoTab, self).__init__(parent)
        self.setupUi(self)
        self.features = lfc.LunarFeatureContainer()
        
    def updateUI(self):
        '''
        This function is for handling things that need to be updated on the 
        UI.
        '''
        self.features.load()
        self.populateLunarIITree()
                
    def populateLunarIITree(self):
        '''
        This function populates the features from the Lunar II Club into the 
        corresponding tree.
        '''
        self.lunar_two_tree.clear()
        self.lunar_two_tree.setColumnCount(2)
        self.lunar_two_tree.setHeaderLabels(["Type/Name", "Latitude"])
        self.lunar_two_tree.setItemsExpandable(True)
        parentFromType = {}
        for feature in self.features.inOrder():
            if feature.code_name in ("LunarII", "Both"):
                ancestor = parentFromType.get(feature.feature_type)
                if ancestor is None:
                    ancestor = QtGui.QTreeWidgetItem(self.lunar_two_tree,
                                                     [feature.feature_type])
                parentFromType[feature.feature_type] = ancestor
                feature_lat_str = StrFmt.ddString(feature.latitude, 2, "latitude")
                item = QtGui.QTreeWidgetItem(ancestor, [feature.name,
                                                        QtCore.QString("%1").arg(feature_lat_str)])
                item.setTextAlignment(1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.lunar_two_tree.expandItem(ancestor)
        self.lunar_two_tree.resizeColumnToContents(0)
        self.lunar_two_tree.resizeColumnToContents(1)
