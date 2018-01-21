"""Executes unittests which require transmission to the target device"""

import socket
import logging
import paramiko
from settings import TARGET, USERNAME, SSH_PORT, PASSWORD, TCP_PORT, INPUT, COMMAND


class ConnectedTest(object):
    """
    :``commands``: - ``list`` - commands is a list of the commands to be executed.  
    If a command is a ``function``, it will be executed.  
    If a command is ``(COMMAND, string)`` it will be sent to the target.  
    If a command is ``(INPUT, 'string')``, user input will be prompted with ``string``.
    """

    def __init__(self, commands):
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

        self.commands = commands

    def start_daemon(self, filename, test):
        """
        Starts the daemon on the target machine. 
        """
        paramiko.util.log_to_file("{}_{}_ssh.log".format(file, test))
        self.sshclient = paramiko.SSHClient()
        self.sshclient.load_system_host_keys()
        self.sshclient.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.sshclient.connect(TARGET, SSH_PORT, USERNAME, PASSWORD)
        transport = self.sshclient.get_transport()
        channel = transport.open_session()
        channel.exec_command("python {} {} {} {}".format(
            filename, test, self.server_address[0], self.server_address[1])) 
            # NOTE: Requires sys.argv
        logging.info("Command sent.")
        logging.info("Starting TCP Server")
        self._exec_test()
        self._kill()

    def _exec_test(self):
        self.socket.listen()
        logging.info("Listening")

        connection, client_address = self.socket.accept()
        log = "Client connected at {}".format(client_address)
        logging.info(log)
        data = connection.recv(16)  # 16 is the number of bytes
        log = "Client ack: %s" % data
        logging.info(log)
        
        response = None
        user_input = ""

        for command in self.commands:
            if callable(command): # checks if command is a function
                logging.info("Local command is being executed")
                command()
                logging.info("Local command executed")
            elif command[0] == COMMAND:
                log = "The command '{}' is being sent to the target".format(command[1])
                logging.info(log)
                connection.sendall(command[1])
                response = connection.recv(16)
                log = "Response received: " + response
                logging.info(log)
            elif command[0] == INPUT:
                log = "User input required, with prompt: " + command[1]
                logging.info(log)
                user_input = raw_input(command[1])
                log = "User inputted " + user_input
                logging.info(log)
        connection.sendall("close")
        connection.close()
        logging.info("All commands have been dealt with")

    
    def _kill(self):
        logging.info("Killing SSH client")
        self.sshclient.close()
        logging.info("SSHClient dead")
