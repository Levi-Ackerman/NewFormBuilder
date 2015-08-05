from task.Task import Task
from main import constant
from xml.dom import minidom
if __name__ == '__main__':
    doc = minidom.parse('../conf.xml')
    constant.instrument_function = doc.getElementsByTagName('instrument_function')[0].firstChild.nodeValue
    constant.instrument_class = doc.getElementsByTagName('instrument_class')[0].firstChild.nodeValue
    constant.repeat_count = doc.getElementsByTagName('repeat_count')[0].firstChild.nodeValue
    instrumentCmd = "adb shell am instrument -w -e class "+constant.instrument_class+"#"+constant.instrument_function+" cn.ninegame.gamemanager/android.test.InstrumentationTestRunner"
    for i in range(int(constant.repeat_count)):
        Task(instrumentCmd,constant.repeat_count).doTest()