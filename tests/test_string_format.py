'''
Created on Apr 23, 2014

@author: Michael Reuter
'''
import unittest
import utils

class StringFormatTest(unittest.TestCase):

    def test_floatString(self):
        # 2-digits precision with negative number
        self.assertEqual(utils.StrFmt.floatString(-0.32421, 2), "-0.32")
        # 2-digits precision with suffix on number
        self.assertEqual(utils.StrFmt.floatString(1.57542, 2, " meters"), "1.58 meters")
    
    def test_ddString(self):
        # North latitude
        self.assertEqual(utils.StrFmt.ddString(31.24654, 2, utils.LATITUDE), 
                         "31.25"+utils.DEGREE_MARKER+" N")
        # South latitude
        self.assertEqual(utils.StrFmt.ddString(-31.24654, 2, utils.LATITUDE), 
                         "31.25"+utils.DEGREE_MARKER+" S")
        # East longitude
        self.assertEqual(utils.StrFmt.ddString(31.24654, 2, utils.LONGITUDE), 
                         "31.25"+utils.DEGREE_MARKER+" E")
        # West longitude
        self.assertEqual(utils.StrFmt.ddString(-31.24654, 2, utils.LONGITUDE), 
                         "31.25"+utils.DEGREE_MARKER+" W")
        
    def test_dmsString(self):
        # Positive DMS tuple
        self.assertEqual(utils.StrFmt.dmsString((15, 30, 20, 1)), 
                         "15"+utils.DEGREE_MARKER+" 30"+utils.ANGLE_MARKERS[1]+" 20"+utils.ANGLE_MARKERS[2])
        # Negative DMS tuple
        self.assertEqual(utils.StrFmt.dmsString((15, 30, 20, -1)), 
                         "-15"+utils.DEGREE_MARKER+" 30"+utils.ANGLE_MARKERS[1]+" 20"+utils.ANGLE_MARKERS[2])
        # Positive DM tuple
        self.assertEqual(utils.StrFmt.dmsString((15, 30, 1)), 
                         "15"+utils.DEGREE_MARKER+" 30"+utils.ANGLE_MARKERS[1])
        # Negative DM tuple
        self.assertEqual(utils.StrFmt.dmsString((15, 30, -1)), 
                         "-15"+utils.DEGREE_MARKER+" 30"+utils.ANGLE_MARKERS[1])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()