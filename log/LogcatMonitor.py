import threading
import datetime
from log.LogListener import LogListener
import subprocess
import json

class LogcatMonitor(threading.Thread):
    adbCmd = "adb logcat -v raw -s FormBuilder:I"
    requestingQuit = False
    logListener = LogListener()
    maxInterval = datetime.timedelta(seconds=5)

    def __init__(self):
        threading.Thread.__init__(self)
        self.timer = threading.Timer(self.maxInterval.seconds,self.timeout)

    def timeout(self):
        if datetime.datetime.now() - self.startTime > self.maxInterval:
            # Time out
            self.stop()
        else :
            self.timer.start()
            pass

    def setLogListener(self,listener):
        self.logListener = listener

    def run(self):
        self.startTime = datetime.datetime.now()
        self.timer.start()
        try:
            print "Begin Listening"
            self.process = subprocess.Popen(self.adbCmd.split(' '),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
            while self.requestingQuit==False and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line.startswith('{'):
                    self.startTime = datetime.datetime.now()
                    print(line)
                    data = json.loads(line)
        except Exception as e:
            print "Catch an exception:"+e
        finally:
            print "Stop Listening"
            pass

    def stop(self):
        self.requestingQuit = True
        if self.isAlive():
            self.process.terminate()
            print "Listening time out!"