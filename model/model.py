# Class to model all data in the MVC design pattern.
# Author: Fernando Abreu e Augusto Rosa
# Date: 11/23/2024
###################################################################################################
# IMPORT
import os
import time
from process import Process, getCpuUsage
from processList import ProcessList
from processHistory import ProcessHistory
from hardwareStats import HardwareStats, STANDARD_TIME_JIFFY
###################################################################################################
# MACROS : podem virar constante de classe com uso da @property
## MACROS para o arquivo /proc/[PID]/stat
PID: int = 0
COMMAND: int = 1
STATE: int = 2
PPID: int = 3
PGRP: int = 4
SESSION: int = 5
TTY_NR: int = 6
TPGID: int = 7
FLAGS: int = 8
MINFLT: int = 9
CMINFLT: int = 10
MAJFLT: int = 11
CMAJFLT: int = 12
UTIME: int = 13
STIME: int = 14
CUTIME: int = 15
CSTIME: int = 16
PRIORITY: int = 17
NICE: int = 18
THREADS: int = 19
ITREALVALUE: int = 20
START_TIME: int = 21
VSIZE: int = 22
RSS: int = 23
RSSLIM: int = 24
START_CODE: int  = 25
END_CODE: int = 26
START_STACK: int = 27
KSTKESP: int = 28
KSTKEIP: int = 29
SIGNAL: int = 30
BLOCKED: int = 31
# ...
## MACROS para o arquivo /proc/[PID]/statm
SIZE: int = 0
RESIDENT: int = 1
SHARED: int = 2
TEXT: int = 3
LIB: int = 4
DATA: int = 5
DIRTY_PAGES: int = 6
## MACROS SISTEMAS
PAGE_SIZE_KB: int = 4
READ: str = "r"
###################################################################################################
# INFORMATION
###################################################################################################

class Model:
    def __init__(self):
        self.__previousProcesses = ProcessList()
        self.__currentProcesses = ProcessList()
        self.history = ProcessHistory()
        self.__hardware_stats = HardwareStats()
        pids = []
        path = "/proc"
        if os.path.exists(path):
            dir_list = os.listdir(path)
            for name_dir in dir_list:
                if name_dir.isdigit():
                    pids.append(name_dir)
        for pid in pids:
            try:
                path = f"/proc/{pid}/stat"
                with open(path, READ) as file:
                    process_info = file.readline().strip().split()
                    execution_time: float = STANDARD_TIME_JIFFY * ( int(process_info[UTIME]) + int(process_info[STIME]) )
                    process: Process = Process(int(process_info[PID]), str(process_info[COMMAND]), str(process_info[STATE]), int(process_info[PPID]), int(process_info[RSS])*PAGE_SIZE_KB, int(process_info[THREADS]), execution_time)
                    self.__currentProcesses.addProcess(process)
            except Exception as e:
                print(f"ERROR({pid}) {path}: {e}")
            if process_info[STATE] == 'S' or process_info[STATE] == 'D':
                try:
                    path = f"/proc/{pid}/wchan"
                    with open(path, READ) as file:
                        process.setWaitChannel(str(file.readline()).strip())
                except Exception as e:
                    print(f"Erro {path}: {e}")
    def getProcessorsInfo(self) -> list:
        return self.__hardware_stats.getProcessorsInfo()
    def getMemoryInfo(self) -> dict:
        return self.__hardware_stats.getMemoryInfo()
    def getCpuUsageCurrent(self) -> str:
        return self.__hardware_stats.getCpuUsageCurrent()
    def getMemoryUsageCurrent(self) -> str:
        return self.__hardware_stats.getMemoryUsageCurrent()
    def getCpuUsage(self) -> list:
        return self.__hardware_stats.getCpuUsage()
    def getMemoryUsage(self) -> list:
        return self.__hardware_stats.getMemoryUsage()
    def setSizeLimit(self, limit: int) -> None:
        self.__hardware_stats.setLimitMetric(limit)
        self.history.setSizeLimit(limit)
    def getSizeLimit(self) -> int:
        return self.history.getSizeLimit()
    def updateHardwareStats(self) -> None:
        self.__hardware_stats.updateStats()
    def updateProcessesByStats(self) -> None:
        if not self.__previousProcesses.empty():
          self.history.addProcessList(self.__previousProcesses)
        self.__previousProcesses = self.__currentProcesses
        self.__currentProcesses = ProcessList()
        pids = []
        path = "/proc"
        if os.path.exists(path):
            dir_list = os.listdir(path)
            for name_dir in dir_list:
                if name_dir.isdigit():
                    pids.append(name_dir)
        for pid in pids:
            try:
                path = f"/proc/{pid}/stat"
                with open(path, READ) as file:
                    process_info = file.readline().strip().split()
                    execution_time: float = STANDARD_TIME_JIFFY * ( int(process_info[UTIME]) + int(process_info[STIME]) )
                    process: Process = Process(int(process_info[PID]), str(process_info[COMMAND]), str(process_info[STATE]), int(process_info[PPID]), int(process_info[RSS])*PAGE_SIZE_KB, int(process_info[THREADS]), execution_time)
                    self.__currentProcesses.addProcess(process)
            except Exception as e:
                print(f"ERROR({pid}) {path}: {e}")
            if process_info[STATE] == 'S' or process_info[STATE] == 'D':
                try:
                    path = f"/proc/{pid}/wchan"
                    with open(path, READ) as file:
                        process.setWaitChannel(str(file.readline()).strip())
                except Exception as e:
                    print(f"Erro {path}: {e}")
            previousProcess = self.__previousProcesses.findProcess(int(pid))
            if previousProcess is not None:
                process.setCpuUsage(getCpuUsage(previousProcess, process))
    def updateProcessesByStatus(self) -> None:
        if not self.__previousProcesses.empty():
          self.history.addProcessList(self.__previousProcesses)
        self.__previousProcesses = self.__currentProcesses
        self.__currentProcesses = ProcessList()
        pids: list = []
        path: str = "/proc"
        if os.path.exists(path):
            dir_list = os.listdir(path)
            for name_dir in dir_list:
                if name_dir.isdigit():
                    pids.append(int(name_dir))
        for pid in pids:
            path = f"/proc/{pid}/status"
            info: dict = {}
            process: Process
            try:
                with open(path, "r") as file:
                    for line in file:
                        index: int = line.find(":")
                        key: str = line[:index].strip()
                        value: str = line[index+1:].strip()
                        info[key] = value
                    info["Pid"] = int(info["Pid"])
                    info["State"] = str(info["State"].split()[0])
                    info["PPid"] = int(info["PPid"])
                    if "VmRSS" not in info:
                        info["VmRSS"] = 0
                    else:
                        info["VmRSS"] = int(info["VmRSS"].split()[0])
                    process = Process(info["Pid"], info["Name"], info["State"], info["PPid"], info["VmRSS"])
                    process.setThreads(int(info["Threads"]))
                    self.__currentProcesses.addProcess(process)
            except Exception as e:
                print(f"Erro updateProcesses2({pid}): {e}")
                continue
            if(info["State"] == 'S' or info["State"] == 'D'):
                path = f"/proc/{pid}/wchan"
                try:
                    with open(path, READ) as file:
                        process.setWaitChannel(str(file.readline()).split())
                except Exception as e:
                    print(f"Erro: {e}")
    def updateProcessesOtherInfo(self) -> None:
        pass
    def update(self):
        self.updateHardwareStats()
        self.updateProcessesByStats()
    def getInfoProcesses(self) -> list:
        return self.__currentProcesses.getInfo()
# end of the class Model

# Test of class or unit test
if __name__=="__main__":
    model: Model = Model()
    time.sleep(1)
    start_time = time.time()
    model.update()
    end_time = time.time()
    info_processes = model.getInfoProcesses()
    cpu_usage_total: float = 0.0
    for p in info_processes:
        info = p.getInfo()
        cpu_usage_total += info[5]
        print(f"{info[0]:^8} {info[1]:^39} {info[2]:^12} {info[3]:^8} {info[4]:^8}  {info[5]*100:^4.1f}%")
        print("")
    print(f"Elapsed Time for update: {(end_time - start_time)*1000:.1f}ms")
    print(f"CPU usage by the sum of each process: {cpu_usage_total*100: .2f}%")
    print(f"CPU usage Total: {model.getCpuUsageCurrent()}")
    print(f"Memory usage: {model.getMemoryUsageCurrent()}")