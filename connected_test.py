"""Executes unittests which require transmission to the target device"""

import socket
import logging
import unittest
import paramiko
from settings import TARGET, USERNAME, SSH_PORT, PASSWORD, TCP_PORT


class ConnectedTest(unittest.TestCase):
    """
    :``commands``: - ``list`` - commands is a list of the commands to be executed.  
    If a command is a ``function``, it will be executed.  
    If a command is ``(COMMAND, string)`` it will be sent to the target.  
    If a command is ``(INPUT, 'string')``, user input will be prompted with ``string``.
    """

    def __init__(self, methodName='runTest'):
        # NOTE: CHECK THIS
        filename = "{}_tcp.log".format(__class__.__name__)
        logging.basicConfig(filename=filename,
                            filemode='w', format='%(asctime): ')

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info("Set up socket")
        hostname = self.socket.gethostbyname()
        logging.info("Acquired hostname")
        self.server_address = (hostname, TCP_PORT)
        logging.info("Acquired server address")
        self.socket.bind(self.server_address)
        logging.info("Bound server address")

        self.sshclient = None
        self.connection = None
        unittest.TestCase.__init__(methodName)

    def start_daemon(self, filename):
        """
        Starts the daemon on the target machine. 
        """
        paramiko.util.log_to_file("{}_ssh.log".format(filename))
        self.sshclient = paramiko.SSHClient()
        self.sshclient.load_system_host_keys()
        self.sshclient.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.sshclient.connect(TARGET, SSH_PORT, USERNAME, PASSWORD)
        transport = self.sshclient.get_transport()
        channel = transport.open_session()
        channel.exec_command("python {} {} {}".format(
            filename, self.server_address[0], self.server_address[1])) 
            # NOTE: Requires sys.argv
        logging.info("Command sent.")
        logging.info("Starting TCP Server")

        self.socket.listen()
        logging.info("Listening")

        self.connection, client_address = self.socket.accept()
        log = "Client connected at {}".format(client_address)
        logging.info(log)
        data = self.connection.recv(16)  # 16 is the number of bytes
        log = "Client ack: %s" % data
        logging.info(log)

        self._kill()

    def send_command(self, command):
        """Sends a command to the target, and returns the response"""
        response = None

        log = "The command '{}' is being sent to the target".format(command)
        logging.info(log)
        self.connection.sendall(command)
        response = self.connection.recv(16)
        log = "Response received: " + response
        logging.info(log)
        
        return response


    
    def _kill(self):
        self.connection.sendall("close")
        self.connection.close()
        logging.info("Target daemon killed")
        logging.info("Killing SSH client")
        self.sshclient.close()
        logging.info("SSHClient dead")
