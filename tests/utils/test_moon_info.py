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
        obs.date = ephem.Date('2013/10/18 18:00:00')
        self.moon = MoonInfo()
        self.moon.compute(obs)

    def test_age(self):
        age = self.moon.age()
        self.assertEquals(age, "13.73")
        
    def test_next_four_phases(self):
        next_phases = self.moon.findNextFourPhases()
        real_phases = [("full", 41564.48448662138), 
                       ("tq", 41572.486443861846), 
                       ("new", 41580.034697486895), 
                       ("fq", 41586.748037173646)]
        
        self.assertEquals(next_phases, real_phases)

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
