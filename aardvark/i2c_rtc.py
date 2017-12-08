"""
This tests the Real Time Clock (RTC) component of a PIM Mini, using the I2C protocol.
These test cases require that a PC is attached to the SDA and SCL lines between the MPU and
I2C components in order to use the Aardvark drivers.
If the PC is running Linux, it is assumed that it is running a 64-bit version.
"""

import unittest
import time
from datetime import datetime, timedelta
from collections import namedtuple
from aardvark_py import aa_open, aa_configure, aa_i2c_pullup, aa_target_power, aa_i2c_bitrate,\
    aa_i2c_bus_timeout, aa_close, aa_i2c_write, aa_i2c_read, AA_CONFIG_GPIO_I2C,\
    AA_I2C_PULLUP_BOTH, AA_TARGET_POWER_BOTH, AA_UNABLE_TO_CLOSE, AA_I2C_WRITE_ERROR,\
    AA_I2C_NO_FLAGS, array
from aardvark_settings import RTC_PORT_NUMBER as PORT_NUMBER, RTC_SLAVE_ADDRESS as SLAVE_ADDRESS,\
    SECONDS_ADDRESS, MINUTE_ADDRESS, HOUR_ADDRESS, DAY_OF_WEEK_ADDRESS, DAY_OF_MONTH_ADDRESS,\
    MONTH_ADDRESS, YEAR_ADDRESS

ClockData = namedtuple("ClockData", [
    "year",
    "month",
    "day_of_month",
    "day_of_week",
    "hours",
    "minutes",
    "seconds"
])


class I2CRTC(unittest.TestCase):  # pylint: disable=R0904
    """
    Tests various scenarios relating to the Real Time Clock (RTC), via the I2C protocol.  
    The tests are numbered to ensure that they are executed in order.
    """

    def __init__(self):
        """Initializer for attributes"""
        super().__init__()
        self.handle = None

    def setUp(self):
        """Is executed before every test"""
        self.handle = aa_open(PORT_NUMBER)
        aa_configure(self.handle, AA_CONFIG_GPIO_I2C)
        aa_i2c_pullup(self.handle, AA_I2C_PULLUP_BOTH)
        aa_target_power(self.handle, AA_TARGET_POWER_BOTH)
        aa_i2c_bitrate(self.handle, 400)  # bitrate = 400
        aa_i2c_bus_timeout(self.handle, 10)  # timeout = 10ms

    @staticmethod
    def b10tob16(value):
        """
        Converts decimal numbers to hexadecimal numbers.  
        Code courtesy of
        [the Linux kernel v4.6](elixir.free-electrons.com/linux/v4.6/source/include/linux/bcd.h).
        """
        return (int(value / 10) << 4) + value % 10

    @staticmethod
    def b16tob10(value):
        """
        Converts hexadecimal numbers to decimal numbers.  
        Code courtesy of
        [the Linux kernel v4.6](elixir.free-electrons.com/linux/v4.6/source/include/linux/bcd.h).
        """
        return ((value) & 0x0f) + ((value) >> 4) * 10

    @staticmethod
    def _write_convert(data):
        """Converts data for writing to the RTC"""
        century_bit = (1 << 7) if (data.year - 1900) > 199 else 0
        data_out = ClockData(
            year=I2CRTC.b10tob16(data.year % 100),
            month=I2CRTC.b10tob16(data.month) | century_bit,
            day_of_month=I2CRTC.b10tob16(data.day_of_month),
            day_of_week=I2CRTC.b10tob16(data.day_of_week),
            hours=I2CRTC.b10tob16(data.hours),
            minutes=I2CRTC.b10tob16(data.minutes),
            seconds=I2CRTC.b10tob16(data.seconds)
        )
        return data_out

    def _write(self, address, value):
        """Method which actually writes to the addresses"""
        data_out = array('B', [address & 0xff, value])
        result = aa_i2c_write(aardvark=self.handle, slave_addr=address,
                              flags=AA_I2C_NO_FLAGS, data_out=data_out)
        self.assertNotEqual(result, AA_I2C_WRITE_ERROR)
        self.assertEqual(result, 1)

    def write(self, data):
        """Writes data to the RTC"""
        data_out = I2CRTC._write_convert(data)
        self._write(YEAR_ADDRESS, data_out.year)
        self._write(MONTH_ADDRESS, data_out.month)
        self._write(DAY_OF_MONTH_ADDRESS, data_out.day_of_month)
        self._write(DAY_OF_WEEK_ADDRESS, data_out.day_of_week)
        self._write(HOUR_ADDRESS, data_out.hours)
        self._write(MINUTE_ADDRESS, data_out.minutes)
        self._write(SECONDS_ADDRESS, data_out.seconds)

    def read(self):
        """Reads data from the RTC and converts it back into the correct format"""
        reg_month = self._read(MONTH_ADDRESS) # this is going to be used twice, so keep it
        data_in = ClockData(
            year=I2CRTC.b16tob10(self._read(YEAR_ADDRESS)) + 100,
            month=I2CRTC.b16tob10(reg_month & 0x1f),
            day_of_month=I2CRTC.b16tob10(self._read(DAY_OF_MONTH_ADDRESS)),
            day_of_week=I2CRTC.b16tob10(self._read(DAY_OF_WEEK_ADDRESS)),
            hours=I2CRTC.b16tob10(self._read(HOUR_ADDRESS) & 0x3f),
            minutes=I2CRTC.b16tob10(self._read(MINUTE_ADDRESS)),
            seconds=I2CRTC.b16tob10(self._read(SECONDS_ADDRESS)),
        )
        if reg_month & (1 << 7):
            data_in.year += 1
        return data_in

    def _read(self, address):
        """Reads an address and returns it"""
        aa_i2c_write(aardvark=self.handle, slave_addr=SLAVE_ADDRESS,
                     flags=AA_I2C_NO_FLAGS, data_out=[address & 0xff])
        count, data_in = aa_i2c_read(
            aardvark=self.handle, slave_addr=address, flags=AA_I2C_NO_FLAGS, data_in=1)
        self.assertEqual(count, 1)
        return data_in[0]

    def check(self, data):
        """
        Checks that the clock can accurately keep the time.  
        : `data` : - The data which will be initially written to the RTC  
        : `delta` : - The time delta after which the RTC will be checked
        """
        delta = timedelta(seconds=10)
        data_formatted = datetime(
            data.year,
            data.month,
            data.day_of_week,
            data.day_of_month,
            data.hours,
            data.minutes,
            data.seconds)

        self.write(data)
        time.sleep(delta.total_seconds)
        data_in = self.read()
        data_in_formatted = datetime(
            data_in.year,
            data_in.month,
            data_in.day_of_week,
            data_in.day_of_month,
            data_in.hours,
            data_in.minutes,
            data_in.seconds)
        check_data = data_formatted + delta
        self.assertEqual(check_data, data_in_formatted)

    def tearDown(self):
        """Is executed after every test"""
        if aa_close(self.handle) == AA_UNABLE_TO_CLOSE:
            raise Exception("The handle failed to close")
        self.handle = None

    def test_01_set_second(self):
        """Checks that the seconds turn over the minute correctly (i.e. mod 60)"""
        data = ClockData(
            year=2017,
            month=12,
            day=8,
            hours=14,
            minutes=0,
            seconds=55
        )
        self.check(data)

    def test_02_set_second_incr(self):
        """Checks that the seconds increment correctly"""
        data = ClockData(
            year=2017,
            month=12,
            day=8,
            hours=14,
            minutes=0,
            seconds=10
        )
        self.check(data)

    def test_03_set_minute(self):
        """Checks that the minutes turn over the hour correctly (i.e. mod 60)"""
        data = ClockData(
            year=2017,
            month=12,
            day=8,
            hours=14,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_04_set_minute_incr(self):
        """Checks that the minutes increment correctly"""
        data = ClockData(
            year=2017,
            month=12,
            day=8,
            hours=14,
            minutes=0,
            seconds=55
        )
        self.check(data)

    def test_05_set_hour_24(self):
        """Checks that the hours turn over the day correctly (i.e. mod 24)"""
        data = ClockData(
            year=2017,
            month=12,
            day=8,
            hours=23,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_06_set_hour_incr_24(self):
        """Checks that the hours increment correctly"""
        data = ClockData(
            year=2017,
            month=12,
            day=8,
            hours=14,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_07_set_day_31(self):
        """Checks that the days turn over the month correctly (i.e. mod 31)"""
        data = ClockData(
            year=2017,
            month=10,
            day=31,
            hours=23,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_08_set_day_30(self):
        """Checks that the days turn over the month correctly (i.e. mod 30)"""
        data = ClockData(
            year=2017,
            month=9,
            day=30,
            hours=23,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_09_set_day_28(self):
        """
        Checks that the days turn over the month correctly for an invalid leap year (i.e. mod 28)  
        """
        data = ClockData(
            year=2017,
            month=2,
            day=28,
            hours=23,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_10_leap_year_div4(self):
        """Checks that the days turn over the month correctly for a valid leap year"""
        data = ClockData(
            year=2004,
            month=2,
            day=28,
            hours=23,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_11_leap_year_div100(self):
        """
        Checks that the days turn over the month correctly for an invalid leap year
        (when the year is divisible by 100)
        """
        data = ClockData(
            year=2100,
            month=2,
            day=28,
            hours=23,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_12_leap_year_div400(self):
        """
        Checks that the days turn over the month correctly for an valid leap year
        (when the year is divisible by 400)
        """
        data = ClockData(
            year=2000,
            month=2,
            day=28,
            hours=23,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_13_set_day_incr(self):
        """Checks that the days increment correctly"""
        data = ClockData(
            year=2017,
            month=12,
            day=8,
            hours=23,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_14_set_month(self):
        """Checks that the months turn over the year correctly"""
        data = ClockData(
            year=2017,
            month=12,
            day=31,
            hours=23,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_15_set_month_incr(self):
        """Checks that the months increment correctly"""
        data = ClockData(
            year=2017,
            month=8,
            day=31,
            hours=23,
            minutes=59,
            seconds=55
        )
        self.check(data)

    def test_16_set_year(self):
        """Checks that the years turn over the century correctly"""
        data = ClockData(
            year=2099,
            month=12,
            day=31,
            hours=23,
            minutes=0,
            seconds=55
        )
        self.check(data)

    def test_17_set_year_incr(self):
        """Checks that the years increment correctly"""
        data = ClockData(
            year=2017,
            month=12,
            day=31,
            hours=23,
            minutes=0,
            seconds=55
        )
        self.check(data)

def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(I2CRTC))
    return suite


def main():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


if __name__ == '__main__':
    main()
