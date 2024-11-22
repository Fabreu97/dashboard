import os
from processHistory import ProcessHistory
from processList import ProcessList
from process import convertToLargestUnit
from process import Process

PID: int = 0
COMMAND: int = 1
STATE: int = 2
PPID: int = 3
RSS: int = 23

class Model:
    def __init__(self) -> None:
        self.currentProcesses = ProcessList()
        self.history = ProcessHistory()
        self.mem_info: dict = {}
        self.processors_info: list = []
    def initialSetup(self) -> None:
        path: str = "/proc/meminfo"
        try:
            with open(path, "r") as file:
                for line in file:
                    index: int = line.find(":")
                    key: str = line[:index]
                    self.mem_info[key] = convertToLargestUnit('KB',int(''.join(filter(str.isdigit, line))))
        except Exception as e:
            print(f"Error {path}: {e}")
        path = f"/proc/cpuinfo"
        try:
            with open(path, "r") as file:
                processor_info: dict = {}
                for line in file:
                    if(line.strip() != ''):
                        index: int = line.find(":")
                        key: str = line[:index].strip()
                        value: str = line[index+1:].strip()
                        if(key == 'processor'):
                            if processor_info:
                                self.processors_info.append(processor_info)
                            processor_info = {}
                        processor_info[key] = value
        except Exception as e:
            print(f"ERROR getInfoProcessor: {e}")
            return None
    def getProcessorInfo(self) -> list:
        return self.processors_info
    def getMemoryInfo(self) -> dict:
        return self.mem_info
    def setSizeLimit(self, limit: int) -> None:
        self.history.setSizeLimit(limit) 
    def getSizeLimit(self) -> int:
        return self.history.getSizeLimit()
    def updateProcesses(self) -> None:
        if self.currentProcesses is not None:
            self.history.addProcessList(self.currentProcesses)
            self.currentProcesses = ProcessList()
        pids = []
        path = "/proc"
        if os.path.exists(path):
            dir_list = os.listdir(path)
            for name_dir in dir_list:
                if name_dir.isdigit():
                    pids.append(name_dir)
        for pid in pids:
            try:
                with open(f"/proc/{pid}/stat") as file:
                    process_info = file.readline().strip().split()
                    self.currentProcesses.addProcess(Process(int(process_info[PID]), str(process_info[COMMAND]), str(process_info[STATE]), int(process_info[PPID]), int(process_info[RSS])))
            except Exception as e:
                print(f"ERROR({pid}): {e}")
        
# end of the class Model