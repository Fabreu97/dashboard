# Class to group a list of processes.
# Author: Fernando Abreu e Augusto Rosa
# Date: 11/26/2024
###################################################################################################
# IMPORT
from .process import Process
###################################################################################################
class ProcessList:
    def __init__(self):
        self.processes: list = []
        self.__R: int = 0 # Running
        self.__S: int = 0 # Sleeping
        self.__D: int = 0 # 
        self.__Z: int = 0 # Zumbi
        self.__T: int = 0 # Stopped
        self.__I: int = 0 # Idle
        self.__U: int = 0 # Unknown
        self.__total_threads: int = 0
    def length(self) -> int:
        return len(self.processes)
    def empty(self) -> bool:
        return self.processes == []
    def getInfo(self) -> list:
        return self.processes
    def addProcess(self, process: Process) -> None:
        character = process.getState()[0]
        if character == "E":
            self.__R += 1
        elif character == "A":
            self.__S += 1
        elif character == "Z":
            self.__Z += 1
        elif character == "P":
            self.__T += 1
        elif character == "I":
            self.__I += 1
        else:
            self.__U += 1
        parent: Process = self.findProcess(process.getParent())
        if parent is not None:
            parent.addProcessChildren(process)
        self.processes.append(process)
        self.__total_threads += process.getThreads()
    def getRunningProcessCount(self) -> int:
        return self.__R
    def getSleepingProcessCount(self) -> int:
        return self.__S
    def getZumbiProcessCount(self) -> int:
        return self.__Z
    def getStoppedProcessCount(self) -> int:
        return self.__T
    def getIdleProcessCount(self) -> int:
        return self.__I
    def getUnknownProcessCount(self) -> int:
        return self.__U
    def findProcess(self, target: int) -> Process | None:
        begin: int = 0
        end: int = len(self.processes) - 1
        flag: bool = False
        position: int = -1
        pid: int = 0
        while( (begin < end) and not flag ):
            position = (begin + end)//2
            pid = self.processes[position].getPID()
            if(pid == target):
                flag = True
            elif(pid > target):
                end = position - 1
            else:
                begin = position + 1
        if(flag):
            return self.processes[position]
        return None
    def findProcessIndex(self, target: int) -> int:
        begin: int = 0
        end: int = len(self.processes) - 1
        flag: bool = False
        position: int = -1
        pid: int = 0
        while( (begin < end) and not flag ):
            position = (begin + end)/2
            pid = self.processes[position].getPID()
            if(pid == target):
                flag = True
            elif(pid > target):
                end = position - 1
            else:
                begin = position + 1
        if(flag):
            return position
        return -1
    def eraseProcess(self, pid: int) -> None:
        position: int = self.findProcessIndex(pid)
        if(position != -1):
            del self.processes[position]
    def cleanProcessList(self) -> None:
        self.processes.clear()
        self.__R = 0
        self.__S = 0
        self.__D = 0
        self.__Z = 0
        self.__T = 0
        self.__I = 0
        self.__U = 0
    def getTotalThreads(self) -> int:
        return self.__total_threads
# end of the class ProcessList
