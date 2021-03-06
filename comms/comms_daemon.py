"""
Daemon which allows the automation of the execution of tests.
Calls comms_target.py
"""

import sys
import os
import socket
import logging
from datetime import datetime, timedelta
import time
import atexit
from signal import SIGTERM
import comms_target


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
        pass


class CommsDaemon(Daemon):
    """
    Automates the execution of the communications tests
    """

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.filename, hostname, tcp_port = sys.argv[1:3] # pylint: disable=E0632
        self.server_address = (hostname, tcp_port)
        self.sock = None
        Daemon.__init__(self, pidfile, stdin, stdout, stderr)

    def test_runner(self):
        """Listens over TCP, executes tests, and returns the results to the controller"""
        command = None
        time_to_stop = datetime.now() + timedelta(minutes=30)
        while command != "close" and time_to_stop > datetime.now():
            command = self.sock.recv(16)
            log = "Received " + command
            logging.info(log)

            comms = None
            result = None
            if command[0] == str(comms_target.CCPComms.__name__):
                comms = comms_target.CCPComms()
            elif command[0] == str(comms_target.IEDComms.__name__):
                comms = comms_target.IEDComms()
                
            if command[1] == "TTL":
                result = comms.test_ttl()
            elif command[1] == "RS-232":
                result = comms.test_rs232()
            elif command[1] == "RS-485":
                result = comms.test_rs485()

            self.sock.sendall(result)
        self.stop()
        
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
    logging.basicConfig(filename="comms_daemon.log", filemode='w', format='%(asctime): ')
    daemon = CommsDaemon('/tmp/comms_daemon.pid')
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
