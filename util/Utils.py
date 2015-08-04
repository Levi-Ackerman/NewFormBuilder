import subprocess,time,datetime

class Utils:
    @staticmethod
    def exeCmdWithTimeout(cmd,timeout):
        # execute a command util time out
        start = datetime.datetime.now()
        process = subprocess.Popen(cmd.split(' '),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        while process.poll() is None:
            time.sleep(0.1)
            if (datetime.datetime.now()-start)>datetime.timedelta(seconds=timeout):
                process.terminate()
        return process.stdout.read()

    @staticmethod
    def exeInstrument(cmd):
        # execute a command to execute instrument in an Android device
        process = subprocess.Popen(cmd.split(' '),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        while process.poll() is None:
            time.sleep(0.1)
            line  = process.stdout.readline()
            print(line)
            if "OK (1 test)" in line:
                process.terminate()
                return True
            elif "FAILURES!!!" in line:
                process.terminate()
                return False