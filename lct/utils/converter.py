# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2012-2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

import math

class Converter(object):
    '''
    This class handles conversion routines.
    '''

    def __init__(self):
        '''
        Constructor. Do nothing as this class will be used statically.
        '''
        pass
    
    @classmethod
    def dmsToDd(cls, dms):
        '''
        This function takes (degrees, minutes, seconds, sign) and turns them into 
        a decimal degree value.
        @param dms: A tuple of four values.
        @return: The decimal degrees of the input.
        '''
        decdeg = dms[0] + (dms[1] / 60.0) + (dms[2] / 3600.0)
        return dms[3] * decdeg
    
    @classmethod
    def ddToDms(cls, decdeg, floatsec=False):
        '''
        This function takes the decimal degrees and returns the equivalent 
        (degrees, minutes, seconds, sign) where sign : [-1, 1].
        @param decdeg: The decimal degrees input.
        @param floatsec: Return seconds as a decimal
        @return: A tuple of four values.
        '''
        # Determine sign
        dms_sign = 1
        if decdeg < 0:
            dms_sign = -1
        # Take out sign as this is now carried above
        decdeg = math.fabs(decdeg)
        degrees = int(decdeg)
        decdeg -= degrees
        decdeg *= 60.0
        minutes = int(decdeg)
        decdeg -= minutes
        decdeg *= 60.0
        if floatsec:
            seconds = decdeg
        else:
            seconds = int(decdeg)
        return (degrees, minutes, seconds, dms_sign)