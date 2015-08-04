from util.Utils import Utils
from log.LogcatMonitor import LogListener,LogcatMonitor
import sqlite3
class Task(LogListener):
    instrumentCmd = "adb shell am instrument -w -e class cn.ninegame.gamemanager.activity.MainActivityTest#testHello cn.ninegame.gamemanager/android.test.InstrumentationTestRunner"
    def __init__(self):
        self.dbconn = sqlite3.connect("my.db",check_same_thread=False)
        self.cursor = self.dbconn.cursor()
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
        self.cursor.execute("create table if not exists agoo(i text)")
        self.cursor.execute("insert into agoo values('"+line["action"]+"')")
        self.dbconn.commit()
