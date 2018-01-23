"""Tests that the LEDs are working, by writing to the appropriate GPIO pins"""

from leds_settings import CCP_OK, IED_OK, FAULT, CCP_DATA_TX, CCP_DATA_RX, IED_DATA_TX, IED_DATA_RX


class LEDHardware(object):
    """Tests that the LEDs are working, by writing to the appropriate GPIO pins"""

    def test_ccp_ok(self):
        """Tests that the CCP OK LED can be turned on"""
        self._test(CCP_OK)

    def test_ied_ok(self):
        """Tests that the IED OK LED can be turned on"""
        self._test(IED_OK)

    def test_fault(self):
        """Tests that the Fault LED can be turned on"""
        self._test(FAULT)

    def test_ccp_data_tx(self):
        """Tests that the CCP Data Tx (transmit) LED can be turned on"""
        self._test(CCP_DATA_TX)

    def test_ccp_data_rx(self):
        """Tests that the CCP Data Rx (receive) LED can be turned on"""
        self._test(CCP_DATA_RX)

    def test_ied_data_tx(self):
        """Tests that the IED Data Tx (transmit) LED can be turned on"""
        self._test(IED_DATA_TX)

    def test_ied_data_rx(self):
        """Tests that the IED Data Rx (receive) LED can be turned on"""
        for i in self._test(IED_DATA_RX):
            yield i # NOTE: make sure that this runs past the yield of _test
        

    def _test(self, pin):
        """Tests an LED"""
        pin.write(True)
        yield pin.read() is True
        pin.write(False)

