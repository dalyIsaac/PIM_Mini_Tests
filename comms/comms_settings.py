"""
Settings for the comms.  
`port` is specified on a separate line to prevent the `Serial` objects from automatically opening.
"""

from serial import Serial, rs485

CCP_TTL = Serial(
    baudrate=384000
)
CCP_TTL.port = ""

CCP_RS232 = Serial(
    baudrate=384000
)
CCP_RS232.port = ""

CCP_RS485 = Serial(
    baudrate=384000
)
CCP_RS485.port = ""
CCP_RS485.rs485_mode = rs485.RS485Settings()

IED_TTL = Serial(
    baudrate=384000
)
IED_TTL.port = ""

IED_RS232 = Serial(
    baudrate=384000
)
IED_RS232.port = ""

IED_RS485 = Serial(
    baudrate=384000
)
IED_RS485.port = ""

TEST_STRING = b"The quick brown fox jumps over the lazy dog 0123456789"
