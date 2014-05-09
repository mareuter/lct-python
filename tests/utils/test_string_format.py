'''
Created on Apr 23, 2014

@author: Michael Reuter
'''
import unittest
import constants

class StringFormatTest(unittest.TestCase):

    def test_floatString(self):
        # 2-digits precision with negative number
        self.assertEqual(constants.StrFmt.floatString(-0.32421, 2), "-0.32")
        # 2-digits precision with suffix on number
        self.assertEqual(constants.StrFmt.floatString(1.57542, 2, " meters"), "1.58 meters")
    
    def test_ddString(self):
        # North latitude
        self.assertEqual(constants.StrFmt.ddString(31.24654, 2, constants.LATITUDE), 
                         "31.25"+constants.DEGREE_MARKER+" N")
        # South latitude
        self.assertEqual(constants.StrFmt.ddString(-31.24654, 2, constants.LATITUDE), 
                         "31.25"+constants.DEGREE_MARKER+" S")
        # East longitude
        self.assertEqual(constants.StrFmt.ddString(31.24654, 2, constants.LONGITUDE), 
                         "31.25"+constants.DEGREE_MARKER+" E")
        # West longitude
        self.assertEqual(constants.StrFmt.ddString(-31.24654, 2, constants.LONGITUDE), 
                         "31.25"+constants.DEGREE_MARKER+" W")
        
    def test_dmsString(self):
        # Positive DMS tuple
        self.assertEqual(constants.StrFmt.dmsString((15, 30, 20, 1)), 
                         "15"+constants.DEGREE_MARKER+" 30"+constants.ANGLE_MARKERS[1]+" 20"+constants.ANGLE_MARKERS[2])
        # Negative DMS tuple
        self.assertEqual(constants.StrFmt.dmsString((15, 30, 20, -1)), 
                         "-15"+constants.DEGREE_MARKER+" 30"+constants.ANGLE_MARKERS[1]+" 20"+constants.ANGLE_MARKERS[2])
        # Positive DM tuple
        self.assertEqual(constants.StrFmt.dmsString((15, 30, 1)), 
                         "15"+constants.DEGREE_MARKER+" 30"+constants.ANGLE_MARKERS[1])
        # Negative DM tuple
        self.assertEqual(constants.StrFmt.dmsString((15, 30, -1)), 
                         "-15"+constants.DEGREE_MARKER+" 30"+constants.ANGLE_MARKERS[1])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()