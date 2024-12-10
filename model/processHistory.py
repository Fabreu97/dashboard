# Class to group a list of processes over time.
# Author: Fernando Abreu e Augusto Rosa
# Date: 12/07/2024
###################################################################################################
# IMPORT
from .process import Process
from .processList import ProcessList
###################################################################################################
# MACROS
SIZE_LIMIT: int = 60
###################################################################################################
class ProcessHistory:
    def __init__(self) -> None:
        self.__history: list = []
        self.__sizeLimit: int = SIZE_LIMIT
    def getInfoCpuUsage(self, pid: int) -> list:
        ans: list = []
        cpu_usage: list = []
        time: list = []
        if len(self.__history) > 0:
            process: Process = self.__history[-1].findProcess(pid)
            while(process is not None):
                cpu_usage.append(process.getCpuUsage())
                time.append(process.getCreationTime())
                process = process.getPreviousProcess()
            ans.append(time)
            ans.append(cpu_usage)
        return ans
    def getInfoMemoryUsage(self, pid: int) -> list:
        ans: list = []
        memory: list = []
        time: list = []
        if len(self.__history) > 0:
            process: Process = self.__history[-1].findProcess(pid)
            while(process is not None):
                memory.append(process.getRSS())
                time.append(process.getCreationTime())
                process = process.getPreviousProcess()
            ans.append(time)
            ans.append(memory)
        return ans   
    def addProcessList(self, old: ProcessList) -> None:
        if(self.__sizeLimit == len(self.__history)):
            del self.__history[0] # oldest
        self.__history.append(old)
    def setSizeLimit(self, limit: int) -> None:
        if (limit > 0):
            self.__sizeLimit = limit
    def getSizeLimit(self) -> int:
        return self.__sizeLimit
# END OF THE CLASS PROCESS_HISTORY