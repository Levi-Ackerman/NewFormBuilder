from util.Utils import Utils
from log.LogcatMonitor import LogListener,LogcatMonitor
class Task(LogListener):
    instrumentCmd = "adb shell am instrument -w -e class cn.ninegame.gamemanager.activity.MainActivityTest#testHello cn.ninegame.gamemanager/android.test.InstrumentationTestRunner"
    def __init__(self):
        self.logcatMonitor = LogcatMonitor()
        self.logcatMonitor.setLogListener(self)
        self.logcatMonitor.start()
    def doTest(self):
        if Utils.exeInstrument(self.instrumentCmd):
            print "test ok"
        else:
            print "test failure"
        self.logcatMonitor.stop(True)
    def onRead(self,line):
        print(line)
