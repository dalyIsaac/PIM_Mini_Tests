"""Contains `CommsTests`, which runs the tests for the comms on the target"""

import unittest
from connected_test import ConnectedTest

class CommsTests(ConnectedTest):
    """Runs the tests for the comms on the target"""

    def __init__(self, methodName="runTest"):
        ConnectedTest.__init__(methodName)
        self.start_daemon("/comms/comms_target.py") # NOTE: check this 

    def test_01_ttl(self):
        """Tests that data can be written and read over TTL"""
        self._test("TTL")

    def test_02_rs232(self):
        """Tests that data can be written and read over RS-232"""
        self._test("RS-232")

    def test_03_rs485(self):
        """Tests that data can be written and read over RS-485"""
        self._test("RS-485")

    def _test(self, test_name):
        status = ""
        while status != "y" and status != "n":
            status = raw_input("Is the PIM Mini ready for the {} {} test? (y/n): ".format(
                self.__class__.__name__, test_name))
            status = status.strip()
        if status == "n":
            self.fail("The user indicated that the test is not ready")
        test_name = (str(self.__class__.__name__), test_name)
        result = self.send_command(test_name)
        if isinstance(result, tuple):
            self.fail(result[1])
        self.assertEqual(result, "True")
    
    def test_04_kill_daemon(self):
        """KILLING DAEMON: NOT A TEST"""
        self._kill()

class CCPComms(CommsTests):
    """CCPComms class"""
    pass


class IEDComms(CommsTests):
    """IEDComms"""
    pass


def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CCPComms))
    suite.addTest(unittest.makeSuite(IEDComms))
    return suite


def run_test_suite():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


def main():
    """Runs the test suite for all of the comms"""
    run_test_suite()


if __name__ == '__main__':
    main()
