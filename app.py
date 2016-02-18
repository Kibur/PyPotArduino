__author__ = 'Kibur'

from arduinoserial import ArduinoSerial
import sys
import time
import threading

class BackgroundWorker(threading.Thread):
    def getObject(self):
        return self._obj

    def getWait(self):
        return self._wait

    def run(self):
        print '"%s" thread started' % (self.getName())

        while not self.stopped():
            try:
                time.sleep(self._wait)

                self.doWork()
            except:
                raise
                self.stop()

        self._obj.write('s')
        self._obj.close()
        print '"%s" is done' % (self.getName())

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def __init__(self, w, obj):
        self._wait = w
        self._obj = obj

        super(BackgroundWorker, self).__init__()
        self._stop = threading.Event()

    def doWork(self):
        line = self._obj.readline()

        if line is not None:
            if ('>' in line) and ('<' in line):
                begin = line.index('>') + 1
                end = line.index('<')
                val = line[begin:end]
                print val
        else: self.stop()

class UI:
    def __init__(self):
        # chmod 666 /dev/tty.usbserial
        arduino = ArduinoSerial('/dev/ttyACM0', 9600)

        bwReadline = BackgroundWorker(0.1, arduino)
        bwReadline.setName('ReadArduino')
        bwReadline.daemon = False
        bwReadline.start()

        arduino.write('g')
        time.sleep(30)

        bwReadline.stop()
        bwReadline.join()

if __name__ == '__main__':
    ui = UI()
