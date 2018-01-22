"""Contains `CommsTests`, which runs the tests for the comms on the target"""

from connected_test import ConnectedTest

class CommsTests(ConnectedTest):
    """Runs the tests for the comms on the target"""

    def test_ttl(self):
        """Tests that data can be written and read over TTL"""
        self._test("TTL")

    def test_rs232(self):
        """Tests that data can be written and read over RS-232"""
        self._test("RS-232")

    def test_rs485(self):
        """Tests that data can be written and read over RS-485"""
        self._test("RS-485")

    def _test(self, test_name):
        status = ""
        while status != "y" and status != "n":
            status = raw_input("Is the PIM Mini ready for the {} {} test? (y/n): ".format(
                self.__class__.__name__, test_name))
            status = status.strip()
        if status == "n":
            self.fail("The user indicated that the test is not ready")
        test_name = (str(self.__class__.__name__), test_name)
        result = self.send_command(test_name)
        if isinstance(result, tuple):
            self.fail(result[1])
        self.assertEqual(result, "True")

class CCPComms(CommsTests):
    """CCPComms class"""
    pass


class IEDComms(CommsTests):
    """IEDComms"""
    pass
