'''
Created on May 11, 2014

@author: Michael Reuter
'''
import unittest

import ephem

from lct.utils.moon_info import MoonInfo

class MoonInfoTestCase(unittest.TestCase):

    def setUp(self):
        obs = ephem.Observer()
        # This is October 18, 2013 6 PM EDT
        obs.date = ephem.Date('2013/10/18 22:00:00')
        self.moon = MoonInfo()
        self.moon.compute(obs)

    def test_age(self):
        age = self.moon.age()
        self.assertEquals(age, "13.89")
        
    def test_next_four_phases(self):
        next_phases = self.moon.findNextFourPhases()
        real_phases = [("full", 41564.48448662116), 
                       ("tq", 41572.486443861955), 
                       ("new", 41580.03469748699), 
                       ("fq", 41586.74803717344)]
        
        self.assertEquals(next_phases, real_phases)
        
    def test_time_from_new_moon(self):
        truth_time_from_new_moon = 333.4247006776859 #hours
        self.assertEquals(self.moon.timeFromNewMoon(), truth_time_from_new_moon)
        
    def test_time_to_new_moon(self):
        truth_time_to_new_moon = 374.8327396878158 #hours
        self.assertEquals(self.moon.timeToNewMoon(), truth_time_to_new_moon)
        
    def test_time_to_full_moon(self):
        truth_time_to_full_moon = 0.06781995449273381 #days
        self.assertEquals(self.moon.timeToFullMoon(), truth_time_to_full_moon)

def suite():
    """
    Return a test suite consisting of all the test cases in the module.
    """
    
    theSuite = unittest.TestSuite()
    theSuite.addTest(unittest.makeSuite(MoonInfoTestCase))
    return theSuite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()