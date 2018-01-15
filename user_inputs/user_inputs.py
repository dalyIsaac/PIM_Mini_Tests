"""Tests that GPIO pins can be written to and read from"""

import unittest
from user_inputs_settings import USER_INPUT_1, USER_INPUT_2, USER_INPUT_3 # pylint: disable=W0403

# List of GPIO pins
USER_INPUTS = [USER_INPUT_1, USER_INPUT_2, USER_INPUT_3]

# Current GPIO pin
USER_INPUT = None


class UserInputs(unittest.TestCase):
    """Tests that values can be written and read from a GPIO pin"""

    def test_high(self):
        """Tests that high values can be written and read from the GPIO pin"""
        USER_INPUT.write(True)
        self.assertEqual(USER_INPUT.read(), True)

    def test_low(self):
        """Tests that low values can be written and read from the GPIO pin"""
        USER_INPUT.write(False)
        self.assertEqual(USER_INPUT.read(), False)


def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UserInputs))
    return suite


def run_test_suite():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


def main():
    """Runs the test suite with the various GPIO pins"""
    for i in USER_INPUTS:
        global USER_INPUT # pylint: disable=W0603
        USER_INPUT = i
        run_test_suite()


if __name__ == '__main__':
    main()
