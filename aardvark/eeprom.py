"""
This tests the EEPROM component of a PIM Mini, using the I2C protocol.
These test cases require that a PC is attached to the SDA and SCL lines between the MPU and
I2C components in order to use the Aardvark drivers.
If the PC is running Linux, it is assumed that it is running a 64-bit version.
"""

import unittest
from array import array
from aardvark_py.aai2c_eeprom import aa_open, aa_configure, aa_i2c_pullup,\
    aa_target_power, aa_i2c_bitrate, aa_i2c_bus_timeout, aa_i2c_write,\
    aa_i2c_read, aa_close, AA_CONFIG_GPIO_I2C, AA_I2C_PULLUP_BOTH,\
    AA_TARGET_POWER_BOTH, AA_I2C_NO_FLAGS, AA_UNABLE_TO_CLOSE
from aardvark_settings import EEPROM_PORT_NUMBER as PORT_NUMBER,\
    EEPROM_PAGE_SIZE as PAGE_SIZE, EEPROM_NUM_PAGES as NUM_PAGES,\
    EEPROM_SLAVE_ADDRESS as SLAVE_ADDRESS, EEPROM_BITRATE as BITRATE
from aardvark_connection import AardvarkConnection


class EEPROMConnection(AardvarkConnection):
    """Tests that the connection of the EEPROM can be configured via I2C"""

    @staticmethod
    def get_port_number():
        """Returns the port number"""
        return PORT_NUMBER

    def configure(self):
        """Tests that the port can be successfully opened and closed"""
        handle_config = aa_configure(self.handle, AA_CONFIG_GPIO_I2C)
        self.assertEqual(handle_config, AA_CONFIG_GPIO_I2C)
        i2c_pullup_resistors = aa_i2c_pullup(self.handle, AA_I2C_PULLUP_BOTH)
        self.assertEqual(i2c_pullup_resistors, AA_I2C_PULLUP_BOTH)
        power_status = aa_target_power(self.handle, AA_TARGET_POWER_BOTH)
        self.assertEqual(power_status, AA_TARGET_POWER_BOTH)
        bitrate = aa_i2c_bitrate(self.handle, BITRATE)  # bitrate = 400
        self.assertEqual(bitrate, BITRATE)
        bus_time_out = aa_i2c_bus_timeout(self.handle, 10)  # timeout = 10ms
        self.assertEqual(bus_time_out, 10)


AardvarkConnection.register(EEPROMConnection)


class EEPROMActions(unittest.TestCase):
    """Tests that the EEPROM can be written to via I2C"""

    def __init__(self, methodName='runTest'):
        """Initializer for attributes"""
        unittest.TestCase.__init__(self, methodName)
        self.handle = None

    def write_memory(self, number):
        """Writes to memory and verifies that the correct amount of data is written"""
        number %= 256  # ensures that the number can be represented with 8-bits, or 1-byte
        # creates a page with a space for the address
        data_out = array('B', [number for _ in range(1 + PAGE_SIZE)])
        for address in range(NUM_PAGES):
            data_out[0] = address & 0xff
            # I'm hoping that Aardvark will assemble the 7-bit slave address,
            # as that's what I think the documentation says
            result = aa_i2c_write(aardvark=self.handle, slave_addr=SLAVE_ADDRESS,
                                  flags=AA_I2C_NO_FLAGS, data_out=data_out)
            self.assertGreater(result, 0)
            self.assertEqual(result, PAGE_SIZE + 1)

    def read_memory(self, number):
        """Reads to memory and verifies that the data read is correct"""
        number %= 256  # ensures that the number can fit inside the 16-bit page size
        for address in range(NUM_PAGES):
            # I'm hoping that Aardvark will assemble the 7-bit slave address,
            # as that's what I think the documentation says
            aa_i2c_write(aardvark=self.handle, slave_addr=SLAVE_ADDRESS,
                         flags=AA_I2C_NO_FLAGS, data_out=array('B', [address & 0xff]))
            count, data_in = aa_i2c_read(
                # I'm hoping that Aardvark will assemble the 7-bit slave address,
                # as that's what I think the documentation says
                aardvark=self.handle, slave_addr=SLAVE_ADDRESS,
                flags=AA_I2C_NO_FLAGS, data_in=PAGE_SIZE
            )
            expected_input = array('B', [number for _ in range(PAGE_SIZE)])
            self.assertEqual(expected_input, data_in)
            self.assertEqual(count, len(expected_input))

    def test_write_read_memory(self):
        """Configures the connection and checks the write and read functionality"""
        self.handle = aa_open(PORT_NUMBER)
        self.assertGreaterEqual(self.handle, 0)
        aa_configure(self.handle, AA_CONFIG_GPIO_I2C)
        aa_i2c_pullup(self.handle, AA_I2C_PULLUP_BOTH)
        aa_target_power(self.handle, AA_TARGET_POWER_BOTH)
        aa_i2c_bitrate(self.handle, BITRATE)
        aa_i2c_bus_timeout(self.handle, 10)  # timeout = 10ms
        for i in range(0, 18, 2):
            self.write_memory(i)
            self.read_memory(i)
        if aa_close(self.handle) == AA_UNABLE_TO_CLOSE:
            raise Exception("The handle failed to close")
        self.handle = None


def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EEPROMConnection))
    suite.addTest(unittest.makeSuite(EEPROMActions))
    return suite


def main():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


if __name__ == '__main__':
    main()
