"""
Defines the abstract class Aardvark Connection, which is used by child classes
to test the I2C and SPI connections.
"""

from abc import ABCMeta, abstractmethod
import unittest
from aardvark_py import aa_find_devices_ext, aa_open, aa_close, AA_PORT_NOT_FREE


class AardvarkConnection(unittest.TestCase):
    """
    Abstract class which is used by child classes to test the I2C and SPI connections.
    """

    __metaclass__ = ABCMeta

    def __init__(self, methodName='runTest'):
        self.port_number = AardvarkConnection.get_port_number()
        self.handle = None
        unittest.TestCase.__init__(self, methodName)

    @staticmethod
    @abstractmethod
    def get_port_number():
        """Returns the port number"""
        pass

    def test_01_port_ready(self):
        """Tests that PORT_NUMBER is connected and available"""
        num, ports, unique_ids = aa_find_devices_ext(16, 16)

        self.assertGreater(num, 0)  # check that devices have been returned
        if num > 0:
            # dictionary of form = port : (unique_id, in_use_status)
            devices = {}
            for i in range(num):
                port, in_use_status = AardvarkConnection.get_status(ports[i])
                devices[port] = unique_ids, in_use_status
            # checks that the port is detected
            self.assertEqual(self.port_number in devices.keys(), True)
            # checks that it's available
            self.assertEqual(devices[self.port_number][1], False)

    @staticmethod
    def get_status(port):
        """Returns the status of the port and the port number"""
        if port & AA_PORT_NOT_FREE:
            port = port & ~AA_PORT_NOT_FREE
            return port, True
        return port, False

    def test_02_open_close(self):
        """Tests that the port can be successfully opened and closed"""
        handle = aa_open(self.port_number)
        self.assertGreater(handle, 0)  # check that the port is open

        self.configure()
        _, status = AardvarkConnection.get_status(self.port_number)
        self.assertEqual(status, False)
        num_closed = aa_close(handle)
        self.assertEqual(num_closed, 1)

    @abstractmethod
    def configure(self):
        """
        Configures the following attributes:
         - handle_config
         - pullup_resistors
         - target_power
         - bitrate
         - bus_timeout
        """
        pass
