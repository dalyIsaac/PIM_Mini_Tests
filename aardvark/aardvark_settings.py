"""Contains the settings for the tests which uses the Aardvark API"""

# EEPROM Settings
EEPROM_PORT_NUMBER = 0
EEPROM_PAGE_SIZE = 16 # NOTE: The number is the number of bytes, per documentation
EEPROM_PAGE_SIZE.__doc__ = "PAGE_SIZE is the number of bytes within a page."
EEPROM_NUM_PAGES = 32 # per documentation
EEPROM_SLAVE_ADDRESS = 0

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
