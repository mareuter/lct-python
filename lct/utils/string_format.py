# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2012-2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

'''
Created on Jun 9, 2012

@author: Michael Reuter
'''
import math

import lct.utils.constants as constants

class StrFmt(object):
    '''
    This is a static class that will handle string formatting
    '''

    def __init__(self):
        '''
        Constructor. Do nothing as this class will be used statically.
        '''
        pass
    
    @classmethod
    def floatString(cls, ifloat, precision, postfix=None):
        """
        This function prints a float as a string with a given precision.
        @param ifloat: The float value to stringify
        @param precision: The number of values after the decimal to print.
        @param postfix: Add a string to the end. Not padded.
        @return: The string representation of the float.
        """
        fmt = "%%.%df" % precision
        istr = fmt % ifloat
        if postfix is not None:
            istr += postfix
        return istr
    
    @classmethod
    def ddString(cls, decdeg, precision, coord_type):
        '''
        This function returns a string representation of a decimal degrees 
        coordinate.
        @param decdeg: The decimal degrees coordinate.
        @param precision: The precision for formatting the coordinate.
        @param coord_type: The particular coordinate type.
        @return: The formatting decimal degree string.
        '''
        dir_tag = ''
        if coord_type == constants.LATITUDE:
            if decdeg < 0:
                decdeg = math.fabs(decdeg)
                dir_tag = "S"
            else:
                dir_tag = "N"
        if coord_type == constants.LONGITUDE:
            if decdeg < 0:
                decdeg = math.fabs(decdeg)
                dir_tag = "W"
            else:
                dir_tag = "E"
                
        dd_str = cls.floatString(decdeg, precision)
        return dd_str + u'\u00b0' + ' ' + dir_tag
    
    @classmethod
    def dmsString(cls, dms):
        '''
        This function takes a DMS tuple (can be DM as well), and returns a 
        string with angle marks for each component. The tuple must contain a last 
        element which is the sign of the value in the set [-1, 1].
        @param dms: A 3 or 4 tuple containing DM or DMS information.
        @return: An angle string with angle marks for each component.
        '''
        astr = ''
        for i, val in enumerate(dms[:-1]):
            astr += str(val) + constants.ANGLE_MARKERS[i] + ' '
        if dms[-1] == -1:
            astr = "-"+astr
        return astr.strip()
    
    @classmethod
    def dateStringNoSeconds(cls, edate, get_local=False):
        '''
        This function converts an ephem.Date object into a date/time string. If one wants local 
        time, the flag get_local may be set to True.
        @param edate: The ephem.Date object.
        @param get_local: Get (or not) the local time from edate.
        @return: The date/time string with no seconds.
        '''
        import ephem
        
        tz_str = ""
        # idate is datetime.datetime
        if get_local:
            idate = ephem.localtime(edate)
            import tzlocal
            tz = tzlocal.get_localzone()
            tz_str = " " + tz.tzname(idate)
        else:
            idate = edate.datetime()
        
        t_str = str(idate.strftime("%Y/%m/%d %H:%M"))
        return t_str + tz_str
        