import threading
import datetime
from log.LogListener import LogListener
import subprocess
import json
from util.Utils import Utils


class LogcatMonitor(threading.Thread):
    adbCmd = "adb logcat -v raw -s ArmlyTool:I"
    requestingQuit = False
    logListener = LogListener()
    maxInterval = datetime.timedelta(seconds=60)

    def __init__(self):
        threading.Thread.__init__(self)

    def runTimer(self):
        self .timer = threading.Timer(self.maxInterval.seconds,self.timeout)
        self.timer.start()

    def timeout(self):
        if datetime.datetime.now() - self.startTime > self.maxInterval:
            # Time out
            self.stop(True)
        else :
            self.runTimer()
            pass

    def setLogListener(self,listener):
        self.logListener = listener

    def run(self):
        self.startTime = datetime.datetime.now()
        Utils.exeCmdWithTimeout("adb logcat -c",5)
        self.runTimer()
        try:
            print "Begin Listening"
            self.process = subprocess.Popen(self.adbCmd.split(' '),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
            while self.requestingQuit==False and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line.startswith('{'):
                    self.startTime = datetime.datetime.now()
                    # print(line)
                    data = json.loads(line)
                    self.logListener.onRead(data)
        except Exception as e:
            print("Catch an exception:"+e.message)
        finally:
            print "Stop Listening"
            pass

    def stop(self,isForce):
        self.requestingQuit = True
        self.timer.cancel()
        if isForce and self.isAlive():
            if self.process :
                self.process.terminate()
            print "Force terminate!"
        self.logListener.onStop()
