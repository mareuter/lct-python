'''
Created on Jun 9, 2012

@author: Michael Reuter
'''
import math
import utils

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
        if coord_type == utils.LATITUDE:
            if decdeg < 0:
                decdeg = math.fabs(decdeg)
                dir_tag = "S"
            else:
                dir_tag = "N"
        if coord_type == utils.LONGITUDE:
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
        string with angle marks for each component.
        @param dms: A 2 or 3 tuple containing DM or DMS information.
        @return: An angle string with angle marks for each component.
        '''
        astr = ''
        for i, val in enumerate(dms):
            astr += str(val) + utils.ANGLE_MARKERS[i] + ' '
        return astr.strip()
        