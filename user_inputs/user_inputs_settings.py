"""
Settings for user_inputs.py.  
NOTE: the pin is the Linux pin number
"""

from periphery import GPIO # pylint: disable=W0403

IN = "in"
OUT = "out"
HIGH = "high"
LOW = "low"
PRESERVE = "preserve"


USER_INPUT_1 = GPIO(pin=0, direction=PRESERVE)
USER_INPUT_2 = GPIO(pin=0, direction=PRESERVE)
USER_INPUT_3 = GPIO(pin=0, direction=PRESERVE)
