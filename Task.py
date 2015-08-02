from util.Utils import Utils

class Task:
    instrumentCmd = "adb shell am instrument -w -e class cn.ninegame.gamemanager.activity.MainActivityTest cn.ninegame.gamemanager/android.test.InstrumentationTestRunner"
    def doTest(self):
        Utils.exeCmd(self.instrumentCmd,5)