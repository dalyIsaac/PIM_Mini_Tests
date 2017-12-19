"""
Connect to the device
"""

import sys
import getpass
import traceback
import socket
import time
import paramiko
from paramiko import SSHException, AuthenticationException, BadHostKeyException, SSHClient
from scp import SCPClient


class Connection(SSHClient):
    """
    Child class of SSHClient. Methods encapsulate argument configuration and connection
    """

    def __init__(self):
        """
        Sets the location of the log file and initiates the SSHClient
        """
        if sys.version_info.major < 3 or sys.version_info.minor < 5:
            raise Exception(
                "Please use Python 3.5 or greater.\nYou are currently using Python {}.{}.{}"
                .format(
                    sys.version_info.major,
                    sys.version_info.minor,
                    sys.version_info.micro
                ))
        paramiko.util.log_to_file("connection.log")
        SSHClient.__init__(self)
        self.load_system_host_keys()
        self.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.shell = None

    def open(self):
        """
        Retrieves the arguments for the connection and connects
        """
        # enable "gssapi-with-mic" authentication, if supported
        use_gss_api = paramiko.GSS_AUTH_AVAILABLE
        # enable "gssapi-kex" key exchange, if supported
        do_gss_api_key_exchange = paramiko.GSS_AUTH_AVAILABLE
        print(" *** Connecting *** ")
        hostname, port, username, password = Connection.configure(
            use_gss_api, do_gss_api_key_exchange)
        try:
            if not use_gss_api and not do_gss_api_key_exchange:
                self.connect(hostname, port, username, password)
            else:
                try:
                    self.connect(hostname, port, username, gss_auth=use_gss_api,
                                 gss_kex=do_gss_api_key_exchange)
                except AuthenticationException:
                    password = getpass.getpass(
                        "Password for {}@{}: ".format(username, hostname))
                    self.connect(hostname, port, username, password)
                except BadHostKeyException as ex:
                    print("Device's host key could not be verified")
                    print("*** Caught exception: %s: %s" % (ex.__class__, ex))
                except SSHException as ex:
                    print("There was an unknown error whilst connecting" +
                          " or establishing an SSH session.")
                    print("*** Caught exception: %s: %s" % (ex.__class__, ex))
                except socket.error as ex:
                    print("There was an error with the socket whilst connecting.")
                    print("*** Caught exception: %s: %s" % (ex.__class__, ex))

            try:
                self.shell = self.invoke_shell()
            except SSHException:
                print("*** The host has failed to start a shell session***")
            print(repr(self.get_transport()))
            print("*** Connected ***")

        except Exception as ex:  # pylint: disable=W0703
            # pylint error is "Catching too general exception Exception"
            print("*** Caught exception: %s: %s" % (ex.__class__, ex))
            traceback.print_exc()
            self.terminate()

    def terminate(self):
        """
        Terminate the shell and the connection
        """
        try:
            self.shell.close()
            self.close()
        except Exception as ex:  # pylint: disable=W0703
            # pylint error is "Catching too general exception Exception"
            print("*** Caught exception: %s: %s" % (ex.__class__, ex))
            print("Most likely related to closing the connection.")
        print("END OF PROGRAM")

    def transmit_text(self, command):
        """
        Transmit inputted text to the device to be executed as a command

        : ``command``: - ``str`` - the command to be sent to the device
        """
        transport = self.get_transport()
        chan = transport.open_session()
        chan.exec_command(command)

        buff_size = 1024
        stdout = []
        while not chan.exit_status_ready():
            time.sleep(1)
            if chan.recv_ready():
                stdout.append(chan.recv(buff_size))

        # Need to gobble up any remaining output after program terminates...
        while chan.recv_ready():
            stdout.append(chan.recv(buff_size))
        stdout = "\n".join([x.decode() for x in stdout])
        stdout = stdout.split("\n")
        stdout.pop()

        return stdout

    def transmit_object(self, name, target_location, is_folder=False):
        """
        Transmit an object to the device. An object is either a file or directory.

        :``name``: - ``str`` - the name of the file/directory to be transmitted

        :``target_location``: - ``str`` -
         the target directory (and filename) for the transmitted object
        """
        file_client = SCPClient(self.get_transport())
        file_client.put(files=name, recursive=is_folder,
                        remote_path=target_location)
        file_client.close()

    @staticmethod
    def configure(use_gss_api, do_gss_api_key_exchange):
        """
        Configures the arguments for the connection

        : ``use_gss_api``: - ``bool`` - enable "gssapi-with-mic" authentication, if supported

        : ``do_gss_api_key_exchange``: - ``bool`` - enable "gssapi-kex" key exchange, if supported
        """
        port = 22

        hostname = input("Hostname: ")
        if not hostname:  # equivalent to len(hostname) == 0
            print("--- ERROR ---")
            print("--- Hostname required ---")
            print("--- END OF PROGRAM ---")
            return None

        try:
            if hostname.find(":") >= 0:  # -1 if not found, index if found
                hostname, portstr = hostname.split(
                    ":")  # resetting port number
                port = int(portstr)
        except ValueError:
            print("--- ERROR ---")
            print("--- Hostname can have a maximum of two colons. ---")
            print("--- END OF PROGRAM ---")
            return None

        username = input("Username: ")
        if not username:  # equivalent to len(username) == 0
            print("--- ERROR ---")
            print("--- You did not input a username. ---")
            print("--- END OF PROGRAM ---")
            return None

        if not use_gss_api and not do_gss_api_key_exchange:
            password = getpass.getpass(
                "Password for {}@{}: ".format(username, hostname))

        return hostname, port, username, password
