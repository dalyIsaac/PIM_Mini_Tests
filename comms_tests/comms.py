"""Tests the serial communications for the PIM_Mini"""

import unittest
from comms_settings import TEST_STRING


class SerialComms(unittest.TestCase):
    """
    Tests the serial communications of the child class.  
    : DO NOT DIRECTLY USE THIS CLASS FOR TESTING.  ALWAYS IMPLEMENT A CHILD CLASS IN THE FORMAT: :
    `class ChildClass(SerialComms): pass`"""

    def __init__(self, methodName="runTest"):
        self.ttl = None
        self.rs232 = None
        self.rs485 = None
        self.configure()
        unittest.TestCase.__init__(self, methodName)

    def configure(self):
        """
        Configures the serial port
        """
        if isinstance(self, CCPComms):
            from comms_settings import CCP_TTL, CCP_RS232, CCP_RS485
            self.ttl = CCP_TTL
            self.rs232 = CCP_RS232
            self.rs485 = CCP_RS485
        elif isinstance(self, IEDComms):
            from comms_settings import IED_TTL, IED_RS232, IED_RS485
            self.ttl = IED_TTL
            self.rs232 = IED_RS232
            self.rs485 = IED_RS485
        else:
            raise Exception("Invalid child class")

    def test_ttl(self):
        """Tests that data can be written and read over TTL"""
        self._test(self.ttl, "TTL")

    def test_rs232(self):
        """Tests that data can be written and read over RS-232"""
        self._test(self.rs232, "RS-232")

    def test_rs485(self):
        """Tests that data can be written and read over RS-485"""
        self._test(self.rs485, "RS-485")

    def _test(self, comm, test_name):
        """Writes, reads, and ensures that the output is correct for the serial device"""
        status = None
        while status != "y" and status != "n":
            status = raw_input(
                "\nIs the PIM Mini ready for the {} {} test? (y/n): "
                .format(self.__class__.__name__, test_name)
            )
            status = status.strip()
        if status == "n":
            self.fail("The user indicated that the test is not ready")
        comm.open()
        comm.write(TEST_STRING)
        output = str(comm.read_all())
        self.assertEqual(output, TEST_STRING)


class CCPComms(SerialComms):
    """CCPComms class"""
    pass


class IEDComms(SerialComms):
    """IEDComms"""
    pass


def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CCPComms))
    suite.addTest(unittest.makeSuite(IEDComms))
    return suite


def main():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


if __name__ == "__main__":
    main()
