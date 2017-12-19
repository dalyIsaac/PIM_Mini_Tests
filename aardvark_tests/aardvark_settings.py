"""Contains the settings for the tests which uses the Aardvark API"""

# EEPROM Settings
EEPROM_PAGE_SIZE = 16 # The number is the number of bytes within a page, per documentation.
EEPROM_NUM_PAGES = 32 # per documentation
EEPROM_PORT_NUMBER = 0
EEPROM_SLAVE_ADDRESS = 80
EEPROM_BITRATE = 400 # in kilohertz

# RTC Settings
RTC_SLAVE_ADDRESS = 0
RTC_PORT_NUMBER = 0
SECONDS_ADDRESS = 0x00
MINUTE_ADDRESS = 0x01
HOUR_ADDRESS = 0x02
DAY_OF_WEEK_ADDRESS = 0x03
DAY_OF_MONTH_ADDRESS = 0x04
MONTH_ADDRESS = 0x05
YEAR_ADDRESS = 0x06
TIME_PERIOD = 600 # time in seconds for test_18_period

# FRAM Settings
FRAM_PORT_NUMBER = 0
FRAM_BITRATE = 1000 # in kilohertz
FRAM_MODE = 0 # SPI mode
FRAM_NUM_ADDRESS = 32768 # assuming that an address is a single 8-bit block
FRAM_INITIAL_ADDRESS = 0
