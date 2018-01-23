"""Contains `LEDsTests`, which runs the tests for the LEDs on the target"""

import unittest
from connected_test import ConnectedTest


class LEDsTests(ConnectedTest):
    """Runs the tests for the LEDs on the target"""

    def __init__(self, methodName="runTest"):
        ConnectedTest.__init__(methodName)
        self.start_daemon("/leds/leds_target.py") # NOTE: check this 

    def test_01_power(self):
        """Tests that when the power is turned on, the power LED is on"""
        actual_power = ""
        while actual_power != "y" and actual_power != "n":
            actual_power = raw_input("\nDoes the device have power? (y/n): ")
        if actual_power == "n":
            self.fail("The device did not have power.")
        led_status = ""
        while led_status != "y" and led_status != "n":
            led_status = raw_input("\nIs the power LED on? (y/n): ")
        self.assertEqual(led_status, "y")

    def test_02_heartbeat(self):
        """Tests that when the device is powered on, the heartbeat LED is flashing"""
        device_on = ""
        while device_on != "y" and device_on != "n":
            device_on = raw_input("\nIs the device on? (y/n): ")
        if device_on == "n":
            self.fail("The user indicated that the device was off. ")
        led_status = ""
        while led_status != "y" and led_status != "n":
            led_status = raw_input("\nIs the heartbeat LED flashing? (y/n): ")
        self.assertEqual(led_status, "y")

    def test_03_ccp_ok(self):
        """Tests that the CCP OK LED can be turned on"""
        self._test("CCP OK")

    def test_04_ied_ok(self):
        """Tests that the IED OK LED can be turned on"""
        self._test("IED OK")

    def test_05_fault(self):
        """Tests that the Fault LED can be turned on"""
        self._test("Fault")

    def test_06_ccp_data_tx(self):
        """Tests that the CCP Data Tx (transmit) LED can be turned on"""
        self._test("CCP Data Tx (transmit)")

    def test_07_ccp_data_rx(self):
        """Tests that the CCP Data Rx (receive) LED can be turned on"""
        self._test("CCP Data Rx (receive)")

    def test_08_ied_data_tx(self):
        """Tests that the IED Data Tx (transmit) LED can be turned on"""
        self._test("IED Data Tx (transmit)")

    def test_09_ied_data_rx(self):
        """Tests that the IED Data Rx (receive) LED can be turned on"""
        self._test("IED Data Rx (receive)")

    def _test(self, test_name):
        result = self.send_command(test_name)
        # result is an indication whether the GPIO assignment was successful
        if not result:
            self.fail("The value for this LED could not be assigned.")
        self.assertEqual(result, "True")
        user_input = raw_input(
            "Is the {} LED turned on?: (y/n): ".format(test_name))
        self.assertEqual(user_input, True)
    
    def test_10_kill_daemon(self):
        """KILLING DAEMON: NOT A TEST"""
        self._kill()


def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LEDsTests))
    return suite


def run_test_suite():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


def main():
    """Runs the test suite for all of the LEDs"""
    run_test_suite()


if __name__ == '__main__':
    main()
