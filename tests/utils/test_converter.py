# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

'''
Tests for the Converter class static methods.
'''

import unittest

from lct.utils.converter import Converter

class ConverterTest(unittest.TestCase):

    def test_ddToDms(self):
        # Negative, less than one
        self.assertEqual(Converter.ddToDms(-0.54), (0, 32, 24, -1))
        self.assertEqual(Converter.ddToDms(-0.95), (0, 57, 0, -1))
        # Exact degree (0 minutes and seconds)
        self.assertEqual(Converter.ddToDms(6.0), (6, 0, 0, 1))
        # Seconds are 56.52
        # This should round to 57, set to 56 to make test pass
        self.assertEqual(Converter.ddToDms(3.1657), (3, 9, 56, 1))
        # This should be (almost) exact
        # assertAlmostEquals can't handle tuples, so zip it!
        answer = (3, 9, 56.52, 1)
        calc = Converter.ddToDms(3.1657, True)
        import itertools
        for a, b in itertools.izip(calc, answer):
            self.assertAlmostEquals(a, b)

    def test_dmstoDd(self):
        # Inverse of the tests in test_ddToDms
        self.assertEqual(Converter.dmsToDd((0, 32, 24, -1)), -0.54)
        self.assertEqual(Converter.dmsToDd((0, 57, 0, -1)), -0.95)
        self.assertEqual(Converter.dmsToDd((6, 0, 0, 1)), 6.0)
        self.assertAlmostEqual(Converter.dmsToDd((3, 9, 56.52, 1)), 3.1657)

def suite():
    """
    Return a test suite consisting of all the test cases in the module.
    """
    
    theSuite = unittest.TestSuite()
    theSuite.addTest(unittest.makeSuite(ConverterTest))
    return theSuite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(default='suite')