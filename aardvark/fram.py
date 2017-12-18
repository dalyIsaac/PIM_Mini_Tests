"""
This tests the FRAM component of a PIM Mini, using the SPI protocol.
If the PC is running Linux, it is assumed that it is running a 64-bit version.
"""

import unittest
from aardvark_py import aa_configure, aa_target_power, aa_spi_configure, aa_spi_bitrate,\
    aa_open, aa_close, aa_spi_write, aa_sleep_ms,\
    AA_CONFIG_SPI_I2C, AA_TARGET_POWER_NONE, AA_SPI_BITORDER_MSB, AA_OK,\
    AA_UNABLE_TO_CLOSE, array, array_u08
from aardvark_connection import AardvarkConnection
from aardvark_settings import FRAM_PORT_NUMBER as PORT_NUMBER, FRAM_BITRATE as BITRATE,\
    FRAM_MODE as MODE, FRAM_INITIAL_ADDRESS as INITIAL_ADDRESS, FRAM_NUM_ADDRESS as NUM_ADDRESS

PAGE_SIZE = 3000


class FRAMConnection(AardvarkConnection):
    """Tests that the connection of the FRAM can be configured via SPI"""

    @staticmethod
    def get_port_number():
        """Returns the port number"""
        return PORT_NUMBER

    def configure(self):
        """Tests that the port can be successfully opened and closed"""
        handle_config = aa_configure(self.handle, AA_CONFIG_SPI_I2C)
        self.assertEqual(handle_config, AA_CONFIG_SPI_I2C)
        power_status = aa_target_power(self.handle, AA_TARGET_POWER_NONE)
        self.assertEqual(power_status, AA_TARGET_POWER_NONE)
        clock_phase = aa_spi_configure(
            self.handle, MODE >> 1, MODE & 1, AA_SPI_BITORDER_MSB)
        self.assertEqual(clock_phase, AA_OK)
        bitrate = aa_spi_bitrate(self.handle, BITRATE)
        self.assertEqual(bitrate, bitrate)


AardvarkConnection.register(FRAMConnection)


class FRAMActions(unittest.TestCase):
    """Tests that the EEPROM can be written to via I2C"""

    def __init__(self, methodName='runTest'):
        """Initializer for attributes"""
        unittest.TestCase.__init__(self, methodName)
        self.handle = None

    def setUp(self):
        """Sets up the tests"""
        self.handle = aa_open(PORT_NUMBER)
        self.assertGreater(self.handle, 0)
        aa_configure(self.handle, AA_CONFIG_SPI_I2C)
        aa_target_power(self.handle, AA_TARGET_POWER_NONE)
        aa_spi_configure(self.handle, MODE >> 1, MODE & 1, AA_SPI_BITORDER_MSB)
        aa_spi_bitrate(self.handle, BITRATE)

    def tearDown(self):
        """Cleans up after the tests"""
        if aa_close(self.handle) == AA_UNABLE_TO_CLOSE:
            raise Exception("The handle failed to close")
        self.handle = None

    def write(self, number, address, size):
        """
        Writes to the FRAM. However, there is an artificial page size enforced, with size
        of 3KB.
        : `number` : - `int` - the number to be sent to the address  
        : `address` : - `int` - the first address to send data to  
        : `size` : - `int` - the number of addresses to write to
        """
        count = 0
        address -= PAGE_SIZE
        while count < size:
            # Send write enable command
            data_out = array('B', [0x06])
            aa_spi_write(self.handle, data_out, 0)

            count += PAGE_SIZE
            address += PAGE_SIZE

            # Assemble data
            data_out = array('B', [number for _ in range(3 + PAGE_SIZE)])
            data_out[0] = 0x02
            data_out[1] = (address >> 8) & 0xff
            data_out[2] = (address >> 0) & 0xff

            if count > size:
                del data_out[(size % PAGE_SIZE) + 3:]

            # Write the transaction
            aa_spi_write(self.handle, data_out, 0)
            aa_sleep_ms(10)

    def read(self, number, address, size):
        """
        Reads from the FRAM. However, there is an artificial page size enforced, with size
        of 3 KB.  
        : `number` : - `int` - the number which should be held in the address  
        : `address` : - `int` - the first address to read data from  
        : `size` : - `int` - the number of addresses to read from
        """
        count = 0
        address -= PAGE_SIZE
        while count < size:

            count += PAGE_SIZE
            address += PAGE_SIZE

            # NOTE: FIX BELOW HERE
            data_out = array('B', [0 for _ in range(3 + size)])
            data_in = array_u08(3 + size)

            # Assemble read command and address
            data_out[0] = 0x03
            data_out[1] = (address >> 8) & 0xff
            data_out[2] = (address >> 0) & 0xff

            if count > size:
                del data_out[(size % PAGE_SIZE) + 3:]

            # Write length+3 bytes for data plus command and 2 address bytes
            (count, data_in) = aa_spi_write(self.handle, data_out, data_in)
            self.assertGreaterEqual(count, 0)
            self.assertEqual(count, size)
            expected_input = array('B', [number for _ in range(count)])
            self.assertEqual(data_in[3:], expected_input)

    def test_write_read_single(self):
        """Writes and then reads from every address, in an interative, singular manner"""
        for i in range(0, 18, 2):
            self.write(i, INITIAL_ADDRESS, 1)
            self.read(i, INITIAL_ADDRESS, 1)

    def test_write_read_overflow(self):
        """Writes and then reads from every address with overflow"""
        for i in range(1, 17, 2):
            self.write(i, INITIAL_ADDRESS, NUM_ADDRESS)
            self.read(i, INITIAL_ADDRESS, NUM_ADDRESS)

def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FRAMConnection))
    suite.addTest(unittest.makeSuite(FRAMActions))
    return suite


def main():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


if __name__ == '__main__':
    main()
