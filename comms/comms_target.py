"""Tests the serial communications for the PIM_Mini"""

from comms_settings import TEST_STRING  # pylint: disable=W0403

class SerialComms():
    """
    Tests the serial communications of the child class.  
    : DO NOT DIRECTLY USE THIS CLASS FOR TESTING.  ALWAYS IMPLEMENT A CHILD CLASS IN THE FORMAT: :
    `class ChildClass(SerialComms): pass`"""

    def __init__(self):
        self.ttl = None
        self.rs232 = None
        self.rs485 = None
        self.configure()

    def configure(self):
        """
        Configures the serial port
        """
        if isinstance(self, CCPComms):
            from comms_settings import CCP_TTL, CCP_RS232, CCP_RS485  # pylint: disable=W0403
            self.ttl = CCP_TTL
            self.rs232 = CCP_RS232
            self.rs485 = CCP_RS485
        elif isinstance(self, IEDComms):
            from comms_settings import IED_TTL, IED_RS232, IED_RS485  # pylint: disable=W0403
            self.ttl = IED_TTL
            self.rs232 = IED_RS232
            self.rs485 = IED_RS485
        else:
            raise Exception("Invalid child class")

    def test_ttl(self):
        """Tests that data can be written and read over TTL"""
        self._test(self.ttl)

    def test_rs232(self):
        """Tests that data can be written and read over RS-232"""
        self._test(self.rs232)

    def test_rs485(self):
        """Tests that data can be written and read over RS-485"""
        self._test(self.rs485)

    def _test(self, comm):
        """Writes, reads, and ensures that the output is correct for the serial device"""
        try:
            comm.open()
            comm.write(TEST_STRING)
            output = str(comm.read_all())
            if output == TEST_STRING:
                return "True"
            return "False"
        except Exception as ex:
            return ("False", ex)


class CCPComms(SerialComms):
    """CCPComms class"""
    pass


class IEDComms(SerialComms):
    """IEDComms"""
    pass
