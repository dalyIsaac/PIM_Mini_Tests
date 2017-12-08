"""
This tests the EEPROM component of a PIM Mini, using the I2C protocol.
These test cases require that a PC is attached to the SDA and SCL lines between the MPU and
I2C components in order to use the Aardvark drivers.
If the PC is running Linux, it is assumed that it is running a 64-bit version.
"""

import unittest
from array import array
from aardvark_py import aa_find_devices_ext, aa_open, aa_configure, aa_i2c_pullup,\
    aa_target_power, aa_i2c_bitrate, aa_i2c_bus_timeout, aa_i2c_write, aa_i2c_read,\
    AA_PORT_NOT_FREE, AA_CONFIG_GPIO_I2C, AA_I2C_PULLUP_BOTH, AA_TARGET_POWER_BOTH,\
    AA_I2C_NO_FLAGS, AA_I2C_WRITE_ERROR
from aardvark_settings import EEPROM_PORT_NUMBER as PORT_NUMBER,\
    EEPROM_PAGE_SIZE as PAGE_SIZE, EEPROM_NUM_PAGES as NUM_PAGES,\
    EEPROM_SLAVE_ADDRESS as SLAVE_ADDRESS


class I2CEEPROMConnection(unittest.TestCase):
    """Tests that the connection of the EEPROM can be configured via I2C"""

    def test_port_ready(self):
        """Tests that PORT_NUMBER is connected and available"""
        num, ports, unique_ids = aa_find_devices_ext(16, 16)

        self.assertGreater(num, 0)  # check that devices have been returned
        if num > 0:
            # dictionary of form = port : (unique_id, in_use_status)
            devices = {}
            for i in range(num):
                port, in_use_status = I2CEEPROMConnection.get_status(ports[i])
                devices[port] = unique_ids, in_use_status
            # checks that the port is detected
            self.assertEqual(PORT_NUMBER in devices.keys(), True)
            # checks that it's available
            self.assertEqual(devices[PORT_NUMBER][1], False)

    @staticmethod
    def get_status(port):
        """Returns the status of the port and the port number"""
        if port & AA_PORT_NOT_FREE:
            port = port & ~AA_PORT_NOT_FREE
            return port, True
        return port, False

    def test_open_close(self):
        """Tests that the port can be successfully opened and closed"""
        handle = aa_open(PORT_NUMBER)
        self.assertLessEqual(handle, 0)  # check that the port is open
        handle_config = aa_configure(handle, AA_CONFIG_GPIO_I2C)
        self.assertEqual(handle_config, AA_CONFIG_GPIO_I2C)
        i2c_pullup_resistors = aa_i2c_pullup(handle, AA_I2C_PULLUP_BOTH)
        self.assertEqual(i2c_pullup_resistors, AA_I2C_PULLUP_BOTH)
        power_status = aa_target_power(handle, AA_TARGET_POWER_BOTH)
        self.assertEqual(power_status, AA_TARGET_POWER_BOTH)
        bitrate = aa_i2c_bitrate(handle, 400)  # bitrate = 400
        self.assertEqual(bitrate, 400)
        bus_time_out = aa_i2c_bus_timeout(handle, 10)  # timeout = 10ms
        self.assertEqual(bus_time_out, 10)
        _, status = self.get_status(PORT_NUMBER)
        self.assertEqual(status, False)


class I2CEEPROMActions(unittest.TestCase):
    """Tests that the EEPROM can be written to via I2C"""

    def __init__(self):
        """Initializer for attributes"""
        super().__init__()
        self.handle = None

    def write_memory(self, number):
        """Writes to memory and verifies that the correct amount of data is written"""
        number %= 256  # ensures that the number can be represented with 8-bits, or 1-byte
        # creates a page with a space for the address
        data_out = array('B', [number for i in range(1 + PAGE_SIZE)])
        for address in range(NUM_PAGES):
            data_out[0] = address & 0xff
            # I'm hoping that Aardvark will assemble the 7-bit slave address,
            # as that's what I think the documentation says
            result = aa_i2c_write(aardvark=self.handle, slave_addr=SLAVE_ADDRESS,
                                  flags=AA_I2C_NO_FLAGS, data_out=data_out)
            self.assertNotEqual(result, AA_I2C_WRITE_ERROR)
            self.assertEqual(result, PAGE_SIZE)

    def read_memory(self, number):
        """Reads to memory and verifies that the data read is correct"""
        number %= 256  # ensures that the number can fit inside the 16-bit page size
        for address in range(NUM_PAGES):
            # I'm hoping that Aardvark will assemble the 7-bit slave address,
            # as that's what I think the documentation says
            aa_i2c_write(aardvark=self.handle, slave_addr=SLAVE_ADDRESS,
                         flags=AA_I2C_NO_FLAGS, data_out=[address & 0xff])
            data_in = [None for _ in range(PAGE_SIZE)]
            count, data_in = aa_i2c_read(
                # I'm hoping that Aardvark will assemble the 7-bit slave address,
                # as that's what I think the documentation says
                aardvark=self.handle, slave_addr=SLAVE_ADDRESS,
                flags=AA_I2C_NO_FLAGS, data_in=PAGE_SIZE
            )
            expected_input = array('B', [number for i in range(1 + PAGE_SIZE)])
            self.assertEqual(expected_input, data_in)
            self.assertEqual(count, len(expected_input))

    def test_write_read_memory(self):
        """Configures the connection and checks the write and read functionality"""
        self.handle = aa_open(PORT_NUMBER)
        aa_configure(self.handle, AA_CONFIG_GPIO_I2C)
        aa_i2c_pullup(self.handle, AA_I2C_PULLUP_BOTH)
        aa_target_power(self.handle, AA_TARGET_POWER_BOTH)
        aa_i2c_bitrate(self.handle, 400)  # bitrate = 400
        aa_i2c_bus_timeout(self.handle, 10)  # timeout = 10ms
        for i in range(0, 16, 2):
            self.write_memory(i)
            self.read_memory(i)


def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(I2CEEPROMConnection))
    suite.addTest(unittest.makeSuite(I2CEEPROMActions))
    return suite


def main():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


if __name__ == '__main__':
    main()
