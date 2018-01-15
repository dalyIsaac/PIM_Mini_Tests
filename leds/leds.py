"""Tests that the LEDs are working, by writing to the appropriate GPIO pins"""

import unittest
from leds_settings import CCP_OK, IED_OK, FAULT, CCP_DATA_TX, CCP_DATA_RX, IED_DATA_TX, IED_DATA_RX


class LEDHardware(unittest.TestCase):
    """Tests that the LEDs are working, by writing to the appropriate GPIO pins"""

    def test_power(self):
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

    def test_heartbeat(self):
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

    def test_ccp_ok(self):
        """Tests that the CCP OK LED can be turned on"""
        self._test(CCP_OK, "CCP OK")

    def test_ied_ok(self):
        """Tests that the IED OK LED can be turned on"""
        self._test(IED_OK, "IED OK")

    def test_fault(self):
        """Tests that the Fault LED can be turned on"""
        self._test(FAULT, "Fault")

    def test_ccp_data_tx(self):
        """Tests that the CCP Data Tx (transmit) LED can be turned on"""
        self._test(CCP_DATA_TX, "CCP Data Tx (transmit)")

    def test_ccp_data_rx(self):
        """Tests that the CCP Data Rx (receive) LED can be turned on"""
        self._test(CCP_DATA_RX, "CCP Data Rx (receive)")

    def test_ied_data_tx(self):
        """Tests that the IED Data Tx (transmit) LED can be turned on"""
        self._test(IED_DATA_TX, "IED Data Tx (transmit)")

    def test_ied_data_rx(self):
        """Tests that the IED Data Rx (receive) LED can be turned on"""
        self._test(IED_DATA_RX, "IED Data Rx (receive)")

    def _test(self, pin, name):
        """Tests an LED"""
        pin.write(True)
        self.assertEqual(pin.read(), False)
        led_status = ""
        while led_status != "y" and led_status != "n":
            led_status = raw_input(
                "\nIs the {} LED turned on? (y/n): ").format(name)
        self.assertEqual(led_status, "y")
        pin.write(False)


def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LEDHardware))
    return suite


def run_test_suite():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


def main():
    """Runs the test suite with the various GPIO pins"""
    run_test_suite()


if __name__ == '__main__':
    main()
