# Class to group a list of processes.
# Author: Fernando Abreu
# Date: 11/23/2024
###################################################################################################
# IMPORT
from process import Process
###################################################################################################
class ProcessList:
    def __init__(self):
        self.processes: list = []
    def empty(self) -> bool:
        return self.processes == []
    def getInfo(self) -> list:
        return self.processes
    def addProcess(self, process: Process) -> None:
        parent: Process = self.findProcess(process.getParent())
        if parent is not None:
            parent.addProcessChildren(process)
        self.processes.append(process)
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
# end of the class ProcessList
