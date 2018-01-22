"""
Daemon which allows the automation of the execution of tests.
Calls leds_target.py
"""

import sys
import os
import socket
import logging
import time
import atexit
from signal import SIGTERM
import leds_target


class Daemon(object):
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork() # pylint: disable=E1101
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, exception:
            sys.stderr.write("fork #1 failed: %d (%s)\n" %
                             (exception.errno, exception.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid() # pylint: disable=E1101
        os.umask(0)

        # do second fork
        try:
            pid = os.fork() # pylint: disable=E1101
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, exception:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (exception.errno, exception.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        sys_in_file = file(self.stdin, 'r')
        sys_out_file = file(self.stdout, 'a+')
        sys_err_file = file(self.stderr, 'a+', 0)
        os.dup2(sys_in_file.fileno(), sys.stdin.fileno())
        os.dup2(sys_out_file.fileno(), sys.stdout.fileno())
        os.dup2(sys_err_file.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        """
        Deletes PID
        """
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pid_file = file(self.pidfile, 'r')
            pid = int(pid_file.read().strip())
            pid_file.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pid_file = file(self.pidfile, 'r')
            pid = int(pid_file.read().strip())
            pid_file.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    print str(err)
            sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been
        daemonized by start() or restart().
        """


class LEDsDaemon(Daemon):
    """
    Automates the execution of the LEDs tests
    """

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.filename, hostname, tcp_port = sys.argv[1:3] # pylint: disable=E0632
        self.server_address = (hostname, tcp_port)
        self.sock = None
        Daemon.__init__(self, pidfile, stdin, stdout, stderr)
    
    def test_runner(self):
        """Listens over TCP, executes tests, and returns the results to the controller"""
        command = None
        while command != "close":
            command = self.sock.recv(16)
            log = "Received " + command
            logging.info(log)

            result = None
            if command == "CCP OK":
                result = leds_target.CCP_OK
            elif command == "IED OK":
                result = leds_target.IED_OK
            elif command == "Fault":
                result = leds_target.FAULT
            elif command == "CCP Data Tx (transmit)":
                result = leds_target.CCP_DATA_TX
            elif command == "CCP Data Rx (receive)":
                result = leds_target.CCP_DATA_RX
            elif command == "IED Data Tx (transmit)":
                result = leds_target.IED_DATA_TX
            elif command == "IED Data Rx (receive)":
                result = leds_target.IED_DATA_RX

            self.sock.sendall(result)

    
    def run(self):
        """Starts listening over TCP, and starts the test runner"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(self.server_address)
            message = "comms_daemon ack"
            self.sock.sendall(message)
            self.test_runner()
        except ValueError as ex:
            log = "Invalid number of arguments:" + ex
            logging.error(log)
            sys.exit(2)

def _main():
    logging.basicConfig(filename="leds_daemon.log", filemode='w', format='%(asctime): ')
    daemon = LEDsDaemon('/tmp/leds_daemon.pid')
    if len(sys.argv) == 2:
        if sys.argv[1] == 'stop':
            daemon.stop()
        elif sys.argv[1] == 'restart':
            daemon.restart()
        else:
            daemon.start()
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

if __name__ == "__main__":
    _main()
