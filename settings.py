"""
Contains:
- Settings and constants for the ``ConnectedTest`` class.
- Boolean values which indicate which tests should be run
"""

SSH_PORT = 22
TCP_PORT = 10000
USERNAME = 'idd17'
PASSWORD = 'Fttokg4A2Egsb0i'
TARGET = '192.168.1.16'

STARTUP_TESTS = True
EEPROM_TESTS = True
FRAM_TESTS = True
RTC_TESTS = True
COMMS_TESTS = True # includes IED and CCP
LEDS_TESTS = True
USER_INPUTS_TESTS = True

