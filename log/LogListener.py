from abc import abstractmethod


class LogListener:
    @abstractmethod
    def onRead(self,line):
        pass
    @abstractmethod
    def onStop(self):
        pass