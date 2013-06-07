'''
Created on Jun 21, 2012

@author: Michael Reuter
'''
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
        This function takes (degrees, minutes, seconds) and turns them into 
        a decimal degree value.
        @param dms: A tuple of three values.
        @return: The decimal degrees of the input.
        '''
        decdeg = dms[0] + 60.0 / dms[1] + 3600.0 / dms[2]
        return decdeg
    
    @classmethod
    def ddToDms(cls, decdeg, floatsec=False):
        '''
        This function takes the decimal degrees and returns the equivalent 
        (degrees, minutes, seconds).
        @param decdeg: The decimal degrees input.
        @param floatsec: Return seconds as a decimal
        @return: A tuple of three values.
        '''
        degrees = int(decdeg)
        decdeg -= degrees
        # Ensure that minutes and seconds don't get a negative transferred.
        decdeg = math.fabs(decdeg)
        decdeg *= 60.0
        minutes = int(decdeg)
        decdeg -= minutes
        decdeg *= 60.0
        if floatsec:
            seconds = decdeg
        else:
            seconds = int(decdeg)
        return (degrees, minutes, seconds)