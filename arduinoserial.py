__author__ = 'Kibur'

import sys
from serial import Serial, SerialException
import time

class ArduinoSerial:
    def getSerialPort(self):
        return self._port

    def getBaudRate(self):
        return self._bps

    def __init__(self, port, bps=9600):
        self._port = port
        self._bps = bps

        try: self._serial = Serial(port, bps, timeout=2)
        except SerialException, se:
            if se.errno is 2:
                print 'Arduino not found!'
                sys.exit(0)
            elif se.errno is 13:
                print 'Permission denied: "%s"' % (port)
                sys.exit(0)

        time.sleep(2)

    def write(self, msg):
        try: self._serial.write(msg.encode(encoding='UTF-8'))
        except SerialException, se:
            if se.errno is 5:
                print 'Write failed to Arduino'
                sys.exit(0)

    def readline(self):
        line = None

        try: line = self._serial.readline()
        except SerialException, se: raise se
        finally: return line

    def close(self):
        self._serial.close()
