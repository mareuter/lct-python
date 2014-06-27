# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

'''
Tests for the MoonInfo class.
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
        self.assertEqual(age, 13.892695861570246)
          
    def test_colongitude(self):
        colong = self.moon.colong()
        self.assertEqual(colong, 1.4655861265848968)
        
    def test_illumination(self):
        illum = self.moon.illumination()
        self.assertEqual(illum, 0.9998519924481626)
        
    def test_libration(self):
        lon_lib = self.moon.libration("long")
        self.assertEqual(lon_lib, 0.09129949120754838)
        lat_lib = self.moon.libration("lat")
        self.assertEqual(lat_lib, -0.025810296625959822)
        
    def test_phase(self):
        phase = self.moon.getPhase()
        self.assertEqual(phase, 3)
        
    def test_phase_name(self):
        phase_name = self.moon.getPhaseAsString()
        self.assertEqual(phase_name, "Waxing Gibbous")
    
    def test_next_four_phases(self):
        next_phases = self.moon.findNextFourPhases()
        real_phases = [("full", 41564.48448662116), 
                       ("tq", 41572.486443861955), 
                       ("new", 41580.03469748699), 
                       ("fq", 41586.74803717344)]
        
        self.assertEqual(next_phases, real_phases)
        
    def test_time_from_new_moon(self):
        truth_time_from_new_moon = 333.4247006776859 #hours
        self.assertEqual(self.moon.timeFromNewMoon(), truth_time_from_new_moon)
        
    def test_time_to_new_moon(self):
        truth_time_to_new_moon = 374.8327396878158 #hours
        self.assertEqual(self.moon.timeToNewMoon(), truth_time_to_new_moon)
        
    def test_time_to_full_moon(self):
        truth_time_to_full_moon = 0.06781995449273381 #days
        self.assertEqual(self.moon.timeToFullMoon(), truth_time_to_full_moon)

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
