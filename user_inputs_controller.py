"""Contains `UserInputsTests`, which runs the tests for the comms on the target"""

import unittest
from connected_test import ConnectedTest


class UserInputsTests(ConnectedTest):
    """
    : THIS IS A BASE CLASS. DO NOT IMPLEMENT THIS CLASS. : 
    Runs the tests for the user inputs on the target
    """

    def __init__(self, methodName="runTest"):
        ConnectedTest.__init__(methodName)
        self.start_daemon("/comms/user_inputs_target.py")  # NOTE: check this

    def test_01_high(self):
        """Tests that high values can be written and read from the GPIO pin"""
        self._test("high")

    def test_02_low(self):
        """Tests that low values can be written and read from the GPIO pin"""
        self._test("low")

    def _test(self, test_name):
        test_name = (str(self.__class__.__name__), test_name)
        result = self.send_command(test_name)
        self.assertEqual(result, "True")

    def test_03_kill_daemon(self):
        """KILLING DAEMON: NOT A TEST"""
        self._kill()


class UserInputOneTests(UserInputsTests):
    """UserInput 1 class"""
    pass


class UserInputTwoTests(UserInputsTests):
    """UserInput 2 class"""
    pass


class UserInputThreeTests(UserInputsTests):
    """UserInput 3 class"""
    pass


def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UserInputOneTests))
    suite.addTest(unittest.makeSuite(UserInputTwoTests))
    suite.addTest(unittest.makeSuite(UserInputThreeTests))
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
