import unittest

class Startup(unittest.TestCase):

    def test_cold_start(self):
        cold_start_status = raw_input("\nDid the device successfully perform a cold startup? ")
        self.assertEqual(cold_start_status, True)
    
    def test_warm_start(self):
        warm_start_status = raw_input("\nDid the device successfully perform a warm startup? ")
        self.assertEqual(warm_start_status, True)
    
    def test_watchdog(self):
        watchdog_status = raw_input("\nIs the watchdog performing as expected? ")
        self.assertEqual(watchdog_status, True)

def construct_test_suite():
    """Constructs the test suite"""
    suite = TestSuite()
    suite.addTest(makeSuite(Startup))
    return suite


def main():
    """Runs the test suite"""
    test_runner = TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


if __name__ == '__main__':
    main()
