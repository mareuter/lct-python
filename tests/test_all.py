'''
Created on May 7, 2014

@author: Michael Reuter

Run all test cases.
'''
import unittest

def suite():
    """
    Make a test suite to run all the tests.
    """
    test_modules = [
                    'tests.utils.test_converter',
                    'tests.utils.test_string_format'
                    ]
    all_tests = unittest.TestSuite()
    for name in test_modules:
        exec('from %s import suite as test_suite' % name)
        all_tests.addTest(test_suite())
    return all_tests

def main():
    unittest.TextTestRunner().run(suite())
    
if __name__ == "__main__":
    main()