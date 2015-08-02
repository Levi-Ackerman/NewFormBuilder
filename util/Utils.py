
class Utils:
    @staticmethod
    def exeCmd(cmd,timeout):
        import subprocess,time,datetime
        start = datetime.datetime.now()
        process = subprocess.Popen(cmd.split(' '),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        while process.poll() is None:
            time.sleep(0.1)
            if (datetime.datetime.now()-start)>datetime.timedelta(seconds=timeout):
                process.terminate()
        return process.stdout.read()