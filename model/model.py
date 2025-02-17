# Class to model all data in the MVC design pattern.
# Author: Fernando Abreu e Augusto Rosa
# Date: 12/07/2024
###################################################################################################
# IMPORT
# from controller.controller import Controller, buffer_general_screen_data
import os
from .process import Process, getCpuUsage, convertToLargestUnit
from .processList import ProcessList
from .processHistory import ProcessHistory
from .hardwareStats import HardwareStats, STANDARD_TIME_JIFFY
import threading
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
MEMORY_TAG = ["Size", "Resident", "Shared", "Text", "Lib", "Data", "Dirty Page"]
###################################################################################################
# VARIABLE GLOBAL
###################################################################################################
# INFORMATION
###################################################################################################

class Model:

    def __init__(self):
        self.__previousProcesses = ProcessList()
        self.__currentProcesses = ProcessList()
        self.__history = ProcessHistory()
        self.__hardware_stats = HardwareStats()
        self.dataReadToSend = threading.Event()
        self.dataReadToSendProcessorScreen = threading.Event() 

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
        self.__history.setSizeLimit(limit)
    def getSizeLimit(self) -> int:
        return self.__history.getSizeLimit()
    def updateHardwareStats(self) -> None:
        self.__hardware_stats.updateStats()
    def updateProcessesByStats(self) -> None:
        if not self.__previousProcesses.empty():
          self.__history.addProcessList(self.__previousProcesses)
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
            '''if process_info[STATE] == 'S' or process_info[STATE] == 'D':
                try:
                    path = f"/proc/{pid}/wchan"
                    with open(path, READ) as file:
                        process.setWaitChannel(str(file.readline()).strip())
                except Exception as e:
                    print(f"Erro {path}: {e}")'''
            previousProcess = self.__previousProcesses.findProcess(int(pid))
            if previousProcess is not None:
                process.setPreviousProcess(previousProcess)
                process.setCpuUsage(getCpuUsage(previousProcess, process))
    def updateProcessesByStatus(self) -> None:
        if not self.__previousProcesses.empty():
          self.__history.addProcessList(self.__previousProcesses)
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
    def update(self):
        self.updateHardwareStats()
        self.updateProcessesByStats()
        self.dataReadToSend.set()
        self.dataReadToSendProcessorScreen.set()
    def getInfoProcesses(self) -> list:
        return self.__currentProcesses.getInfo()
    def getHistoryCpuUsage(self, pid: int) -> list:
        return self.__history.getInfoCpuUsage(pid)
    def dataProcessScreen(self, pid) -> list:
        data = []
        path = f"/proc/{pid}"
        try:
            if os.path.exists(path):
                # Obtendo arquivos abertos pelo processo
                try:
                    open_files = len(os.listdir(f"/proc/{pid}/fd"))
                except Exception:
                    open_files = 0
                try:
                    with open(f"/proc/{pid}/io", "r") as f:
                        io_stats = {}
                        for line in f:
                            key, value = line.split(":")
                            io_stats[key.strip()] = int(value.strip())
                except Exception:
                    io_stats = {}
                # Obtendo quantidade de sockets abertos pelo processo
                try:
                    with open(f'/proc/{pid}/net/tcp', 'r') as f:
                        sockets_tcp = 0
                        for line in f.readlines()[1:]:
                            sockets_tcp = sockets_tcp+1
                except Exception:
                    sockets_tcp = 0
                try:
                    with open(f'/proc/{pid}/net/udp', 'r') as f:
                        sockets_udp = 0
                        for line in f.readlines()[1:]:
                            sockets_udp = sockets_udp+1
                except Exception:
                    sockets_udp = 0

                try:
                    ipc_dir = f'/proc/{pid}/task'
                    if(os.path.exists(ipc_dir)):
                        for task in os.listdir(ipc_dir):
                            try:
                                with open(f'{ipc_dir}/{task}/status', 'r') as f:
                                    sem_and_mut = 0
                                    for line in f:
                                        if line.startswith("SigPnd:") or line.startswith("ShdPnd:"):
                                            sem_and_mut = sem_and_mut+1
                            except FileNotFoundError:
                                continue
                except FileNotFoundError:
                    print(f"Não foi possível acessar /proc/{pid}/task.")
                    sem_and_mut = 0
                except Exception:
                    sem_and_mut = 0

                try:
                    with open(f"/proc/{pid}/statm", "r") as f:
                        memory_proc_info = {}
                        for line in f:
                            value = line.split()
                        for i in range(len(MEMORY_TAG)):
                            memory_proc_info[MEMORY_TAG[i]] = int(value[i])
                except Exception:
                    memory_proc_info = {}

                data.append(open_files)
                data.append(io_stats)
                data.append(sockets_tcp)
                data.append(sockets_udp)
                data.append(sem_and_mut)
                data.append(memory_proc_info)
                return data
            else:
                return None
        except Exception:
            print("Erro")
            return([])

    def getHistoryRSS(self, pid: int) -> list:
        return self.__history.getInfoMemoryUsage()
    def dataRequestFromTheGeneralScreen(self) -> None:
        # importando o buffer
        from controller.controller import buffer_general_screen_data
        # monta os dados no formato que tela Geral possa consumir
        while(True):
            self.dataReadToSend.wait()
            data: list = []
            # Montando o pacote de dados a ser enviado . . .
            data.append(self.__currentProcesses.length()) # 0
            data.append(self.__currentProcesses.getInfo()) # 1
            data.append(self.__hardware_stats.getCpuUsageCurrent()) # 2
            data.append(self.__hardware_stats.getMemoryUsageCurrent()) # 3
            data.append(convertToLargestUnit('KB', int(self.__hardware_stats.getMemoryInfo()['MemTotal']))) # 4
            data.append(self.__currentProcesses.getTotalThreads()) # 5
            data.append(self.__currentProcesses.getRunningProcessCount()) #6
            data.append(self.__currentProcesses.getSleepingProcessCount()) # 7
            data.append(self.__currentProcesses.getZumbiProcessCount()) # 8
            data.append(self.__currentProcesses.getStoppedProcessCount()) # 9
            data.append(self.__currentProcesses.getIdleProcessCount()) # 10
            data.append(self.__hardware_stats.getProcessorCore()) # 11
            data.append(self.__hardware_stats.getVersionOS()) # 12
            buffer_general_screen_data.put(data) # enviar
            print("Model está enviando os dados da Tela Geral...")
            self.dataReadToSend.clear()

    def dataRequestFromTheProcessorDetailsScreen(self) -> None:
        # importar o buffer
        from controller.controller import buffer_processor_details_screen_data
        while(True):
            self.dataReadToSendProcessorScreen.wait()
            # Montando o pacores de dados a ser enviado . . .
            data = []
            data.append(self.__hardware_stats.getCpuUsage()) # 1
            # Enviando os dados
            buffer_processor_details_screen_data.put(data)
            print("Model está enviando os dados da Tela de Detalhes do Processador...")
            self.dataReadToSendProcessorScreen.clear()
    

# end of the class Model