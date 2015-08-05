from util.Utils import Utils
from log.LogcatMonitor import LogListener,LogcatMonitor
import sqlite3
class Task(LogListener):
    instrumentCmd = "adb shell am instrument -w -e class cn.ninegame.gamemanager.activity.MainActivityTest#testHello cn.ninegame.gamemanager/android.test.InstrumentationTestRunner"
    def __init__(self):
        # init dbconnect
        self.dbconn = sqlite3.connect("my.db",check_same_thread=False)
        self.cursor = self.dbconn.cursor()

        tabletuple = self.cursor.execute("select name from sqlite_master where type = 'table'").fetchall()
        self.tablenames = [tb[0] for tb in tabletuple]

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
        if line.has_key('action') is False:
            return
        print(line)
        action = line.pop('action')
        keys = line.keys()
        values = line.values()
        count = len(keys)
        if action not in self.tablenames:
            self.tablenames.append(action)
            create_sql = 'create table if not exists '+action+' ('+','.join(['{} text'.format(column) for column in keys])+')'
            self.cursor.execute(create_sql)
        insert_sql = 'insert into '+action+' ('+(','.join(keys))+') values ('+(','.join(values))+")"
        self.cursor.execute(insert_sql)
        self.dbconn.commit()
    def onStop(self):
        self.cursor.close()
        self.dbconn.close()