"""
This tests the startup processes of a PIM Mini.
These tests rely on user input to determine the passing of the tests
"""

import unittest

class Startup(unittest.TestCase):
    """Tests the startup processes of a PIM Mini"""

    def test_cold_start(self):
        """Tests that a cold start can successfully occur"""
        cold_start_status = raw_input("\nDid the device successfully perform a cold startup? ")
        self.assertEqual(cold_start_status, True)
    
    def test_warm_start(self):
        """Tests that a warm start can successfully occur"""        
        warm_start_status = raw_input("\nDid the device successfully perform a warm startup? ")
        self.assertEqual(warm_start_status, True)
    
    def test_watchdog(self):
        """Ensures that the watchdog is performing as expected"""        
        watchdog_status = raw_input("\nIs the watchdog performing as expected? ")
        self.assertEqual(watchdog_status, True)

def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Startup))
    return suite


def main():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


if __name__ == '__main__':
    main()
