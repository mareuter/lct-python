# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

'''
Tests for the ObservingSite class methods.
'''

import unittest

from lct.utils.observing_site import ObservingSite

class ObservingSiteTest(unittest.TestCase):

    def setUp(self):
        self.datestr = "2014/10/18"
        # Midnight, 6 AM, Noon and 6 PM fail the test!
        self.timestr = "19:00:00"

    def test_standardConstruction(self):
        obs_site = ObservingSite()
        self.assertIsNotNone(obs_site.getDateTime())
        
    def test_timeStringConstruction(self):
        obs_site = ObservingSite()
        obs_site.setDateTime(" ".join([self.datestr, self.timestr]))
        datetimestr = "T".join([self.datestr, self.timestr]).replace('/', '-')
        self.assertEquals(obs_site.getDateTime(), datetimestr)

def suite():
    """
    Return a test suite consisting of all the test cases in the module.
    """
    
    theSuite = unittest.TestSuite()
    theSuite.addTest(unittest.makeSuite(ObservingSiteTest))
    return theSuite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(default='suite')