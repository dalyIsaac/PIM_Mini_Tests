"""
Settings for leds.py.  
NOTE: the pin is the Linux pin number
"""

from periphery import GPIO  # pylint: disable=W0403

IN = "in"
OUT = "out"
HIGH = "high"
LOW = "low"
PRESERVE = "preserve"

CCP_OK = GPIO(pin=0, direction=PRESERVE)
IED_OK = GPIO(pin=0, direction=PRESERVE)
FAULT = GPIO(pin=0, direction=PRESERVE)
CCP_DATA_TX = GPIO(pin=0, direction=PRESERVE)
CCP_DATA_RX = GPIO(pin=0, direction=PRESERVE)
IED_DATA_TX = GPIO(pin=0, direction=PRESERVE)
IED_DATA_RX = GPIO(pin=0, direction=PRESERVE)
