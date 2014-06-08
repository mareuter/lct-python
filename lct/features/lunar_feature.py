# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2012-2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

import os

from PyQt4 import QtCore

class LunarFeature(object):
    '''
    This class is responsible for holding the information for a given lunar 
    feature.
    '''

    def __init__(self, name, latitude, longitude, feature_type,
                 delta_latitude, delta_longitude, code_name, club_type):
        '''
        Constructor
        '''
        self.name = QtCore.QString(name)
        self.latitude = latitude
        self.longitude = longitude
        self.feature_type = QtCore.QString(feature_type)
        self.delta_latitude = delta_latitude
        self.delta_longitude = delta_longitude
        self.code_name = QtCore.QString(code_name)
        self.club_type = QtCore.QString(str(club_type))
        
    def __str__(self):
        '''
        This function produces the string representation of the lunar feature.
        @return: The string representation.
        '''
        result = []
        result.append("Name = %s" % self.name)
        result.append("Lat/Long = (%.2lf, %.2lf)" % (self.latitude, self.longitude))
        result.append("Type = %s" % self.feature_type)
        result.append("Delta Lat/Long = (%.2lf, %.2lf)" % (self.delta_latitude, self.delta_longitude))
        return os.linesep.join(result)
    
    def __repr__(self):
        '''
        This function produces the pickleable format for the lunar feature.
        @return: The object representation.
        '''
        return self.__str__()