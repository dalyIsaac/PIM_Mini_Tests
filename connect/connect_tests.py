"""
Tests the functionality of modules which are executed locally.
Methods in Python are stored in a dictionary, which is ordered alphabetically in Python 3.6.
i.e. test_transmit_text will always be executed after test_init.
"""

import sys

# Ensure that this is running in Python 3.5+
if sys.version_info.major < 3 or sys.version_info.minor < 5:
    raise Exception(
        "Please use Python 3.5 or greater.\nYou are currently using Python {}.{}.{}"
        .format(
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro
        ))
else:
    import unittest
    from unittest.mock import patch  # python 3+
    from os import path
    import io
    from connect_tests_settings import HOSTNAME, USERNAME, PASSWORD  # python 3+
    from connect import Connection


class ConnectionMethods(unittest.TestCase):
    """Tests the methods of the Connection class which are not inherited"""

    def test_init(self):
        """Tests that the log is created"""
        c_var = Connection()
        self.assertIsInstance(c_var, Connection)
        filename = "connection.log"
        self.assertEqual(path.exists(filename) and path.isfile(filename), True)

    @staticmethod
    def configure_setup():
        """Configures the setup for other methods"""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        configuration = Connection.configure(False, False)
        captured_output = captured_output.getvalue().split('\n')
        sys.stdout = sys.__stdout__
        return configuration, captured_output

    @patch('builtins.input', side_effect=[''])
    def test_configure_hostname_size(self, _):
        """Ensures that the configuration fails with an invalid hostname (no hostname entered)"""
        configuration, captured_output = ConnectionMethods.configure_setup()
        self.assertEqual(configuration, None)
        self.assertEqual(captured_output[0:2], [
            "--- ERROR ---", "--- Hostname required ---"])

    @patch('builtins.input', side_effect=['::'])
    def test_configure_hostname_colon(self, _):
        """Ensures that the configuration fails with an invalid hostname (has extra colons)"""
        configuration, captured_output = ConnectionMethods.configure_setup()
        self.assertEqual(configuration, None)
        self.assertEqual(captured_output[0:2], [
            "--- ERROR ---", "--- Hostname can have a maximum of two colons. ---"])

    @patch('builtins.input', side_effect=['192.168.1.1', ''])
    def test_configure_invalid_username(self, _):
        """Ensures that the configuration fails with no username entered"""
        configuration, captured_output = ConnectionMethods.configure_setup()
        self.assertEqual(configuration, None)
        self.assertEqual(captured_output[0:2], [
            "--- ERROR ---", "--- You did not input a username. ---"])

    @patch('builtins.input', side_effect=['192.168.1.1', 'helloworld'])
    @patch('getpass.getpass', side_effect=['password'])
    def test_configure_valid(self, _, __):
        """Ensures that the configuration succeeds when the configuration is valid"""
        configuration, _ = ConnectionMethods.configure_setup()
        self.assertNotEqual(configuration, None)
        self.assertEqual(len(configuration), 4)

    @patch('builtins.input', side_effect=[HOSTNAME, USERNAME])
    @patch('getpass.getpass', side_effect=[PASSWORD])
    def test_open_close(self, _, __):
        """Tests that the connection can be successfully opened and closed"""
        # NOTE: THIS RELIES ON ACCURATE DATA RESIDING IN test_values.py
        captured_output = io.StringIO()  # captures output
        sys.stdout = captured_output
        c_var = Connection()
        c_var.open()
        self.assertEqual(c_var.get_transport().is_active(), True)
        """This assumes that c_var.get_transport.is_active() is accurate. There have been
         reports that it returns false positives.
         See:
         https://stackoverflow.com/questions/28288533/check-if-paramiko-ssh-connection-is-still-alive
         Alternative is commented below"""
        # self.assertEqual(self._alternative_test_open_close(), False)
        c_var.terminate()
        self.assertEqual(c_var.get_transport(), None)

    # def _alternative_test_open_close(self):
        # """Tests that the connection can be successfully opened and closed"""
        # send_ignore_status_success = True
        # try:
        #     transport = c_var.get_transport()
        #     transport.send_ignore()
        # except EOFError:
        #     send_ignore_status_success = False
        # return send_ignore_status_success

    @patch('builtins.input', side_effect=[HOSTNAME, USERNAME])
    @patch('getpass.getpass', side_effect=[PASSWORD])
    def test_transmit_command(self, _, __):
        """Ensures that a command can be successfully sent, with the output read"""
        c_var = Connection()
        c_var.open()
        stdout = c_var.transmit_text('ls /')
        std_linux_root = 'bin  boot  dev  etc  home  lib  lost+found  media  \
        mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var'
        std_linux_root = [
            i for i in std_linux_root.split(" ") if i.strip() != ""]
        self.assertEqual(stdout, std_linux_root)
        c_var.terminate()

    @patch('builtins.input', side_effect=[HOSTNAME, USERNAME])
    @patch('getpass.getpass', side_effect=[PASSWORD])
    def test_transmit_object(self, _, __):
        """
        Ensures that an object can be successfully sent.
        This test relies on test_transmit_command being successful.
        Due to the way that Python dictionaries work, test_transmit_command is
        going to be executed prior to test_transmit_object
        """
        c_var = Connection()
        c_var.open()
        c_var.transmit_object("Tests/testfile.py", "/home/user/testfile.py")
        stdout = c_var.transmit_text('ls /home/user/ | grep testfile.py')
        self.assertEqual(stdout[0], "testfile.py")
        c_var.terminate()


def construct_test_suite():
    """Constructs the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConnectionMethods))
    return suite


def main():
    """Runs the test suite"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(construct_test_suite())


if __name__ == '__main__':
    main()
