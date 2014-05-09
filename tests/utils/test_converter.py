'''
Created on Apr 23, 2014

@author: Michael Reuter
'''
import unittest
import constants

class UtilsTest(unittest.TestCase):

    def test_ddToDms(self):
        # Negative, less than one
        self.assertEqual(constants.Converter.ddToDms(-0.54), (0, 32, 24, -1))
        self.assertEqual(constants.Converter.ddToDms(-0.95), (0, 57, 0, -1))
        # Exact degree (0 minutes and seconds)
        self.assertEqual(constants.Converter.ddToDms(6.0), (6, 0, 0, 1))
        # Seconds are 56.52
        # This should round to 57, set to 56 to make test pass
        self.assertEqual(constants.Converter.ddToDms(3.1657), (3, 9, 56, 1))
        # This should be (almost) exact
        # assertAlmostEquals can't handle tuples, so zip it!
        answer = (3, 9, 56.52, 1)
        calc = constants.Converter.ddToDms(3.1657, True)
        import itertools
        for a, b in itertools.izip(calc, answer):
            self.assertAlmostEquals(a, b)

    def test_dmstoDd(self):
        # Inverse of the tests in test_ddToDms
        self.assertEqual(constants.Converter.dmsToDd((0, 32, 24, -1)), -0.54)
        self.assertEqual(constants.Converter.dmsToDd((0, 57, 0, -1)), -0.95)
        self.assertEqual(constants.Converter.dmsToDd((6, 0, 0, 1)), 6.0)
        self.assertAlmostEqual(constants.Converter.dmsToDd((3, 9, 56.52, 1)), 3.1657)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()