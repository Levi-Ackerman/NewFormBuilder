
class Utils:
    def exeCmd(self,cmd,timeout):
        import subprocess,time,datetime
        start = datetime.datetime.now()
        process = subprocess.Popen(cmd.split(' '),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        while process.poll() is None:
            #不断读命令的输出
            time.sleep(0.1)
            if (datetime.datetime.now()-start)>timeout:
                #输出太多太久，不读了，直接断开
                process.terminate()
        return process.stdout.read()