# Class to group the information of a process.
# Author: Fernando Abreu
# Date: 11/23/2024
###################################################################################################
# IMPORT
import time
###################################################################################################
# MACROS:
STORAGE_UNITS = ("B", "KB", "MB", "GB", "TB")
###################################################################################################
# TODO: find a way to find uot how much time a process consumes on the Process class
###################################################################################################
#   PID : ID do processo
#   Command or Name: nome do processo
#   State: estado do processo
#       - R: Running    -> executando
#       - S: Sleeping   -> esperando algum recurso, pode descobrir observado wchan
#       - D: 
#       - Z: Zumbi      -> termino de ser executado, mas ainda não foi removido na tabela de processos
#       - T: Stopped    -> processo paralizado
#       - I: Idle       -> processo inativo
#   PPID: (Parent Process ID)Processo pai
#   RSS: (Resident Set Size)uso de memoria residente(stats é dado por páginas e status é dado em KB)
#   wchan: (Wait Channel)canal de espera, mostra o que o processo esta aguardando
#   cmdline: linha de comando da execução do processo
#   threads: Número de threads no processo
###################################################################################################
class Process:
    def __init__(self, PID : int, command: str, state: str, PPID: int, RSS: int, threads: int = 1, execution_time: float = 0.0):
        self.__PID = PID
        self.__command = command
        if (state=='R'):
            self.__state = "Execução"
        elif(state == 'S' or state == 'D'):
            self.__state = "Aguardando"
        elif(state == 'Z'):
            self.__state = "Zumbi"
        elif(state == 'T'):
            self.__state = "Paralisado"
        elif(state == 'I'):
            self.__state = "Inativo"
        else:
            self.__state = "Desconhecido"
        self.__PPID = PPID
        self.__RSS = RSS
        self.__memory = convertToLargestUnit('KB', RSS)
        self.__children: list = []
        self.__wchan = ""
        self.__cmdline = ""
        self.__threads = threads
        self.__execution_time = execution_time
        self.__creation_time = time.time()
        self.__cpu_usage: float = 0.0
    def getPID(self) -> int:
        return self.__PID
    def getCommand(self) -> str:
        return self.__command
    def getState(self) -> str:
        return self.__state
    def getParent(self) -> int:
        return self.__PPID
    def getRSS(self) -> int:
        return self.__RSS
    def getMemory(self) -> str:
        return self.__memory
    def getInfo(self) -> list:
        return [self.__PID, self.__command, self.__state, self.__PPID, self.__memory, self.__cpu_usage]
    def addProcessChildren(self, process) -> None:
        self.__children.append(process)
    def setWaitChannel(self, wchan: str) -> None:
        self.__wchan = wchan
    def getWaitChannel(self) -> str:
        return self.__wchan
    def setCommandLine(self, cmdline: str) -> None:
        self.__cmdline = cmdline
    def getCommandLine(self) -> str:
        return self.__cmdline
    def setThreads(self, threads: int) -> None:
        self.__threads = threads
    def getThreads(self) -> int:
        return self.__threads
    def setExecutionTime(self, time: float) -> None:
        self.__execution_time = time
    def getExecutionTime(self) -> float:
        return self.__execution_time
    def getCreationTime(self) -> float:
        return self.__creation_time
    def setCpuUsage(self, cpu_usage: float) -> None:
        self.__cpu_usage = cpu_usage
    def getCpuUsage(self) -> float:
        return self.__cpu_usage
# end of the class Process

def convertToLargestUnit(cmc: str, value: int) -> str:
    result: str = ""
    try:
        i = STORAGE_UNITS.index(cmc)
    except ValueError:
        print(f"Elemento não encontrado: {cmc}")
        return "Erro convertToLargestUnit"
    v = value
    while(float(v/1024) >= 1.0):
        v = v/1024
        i += 1
    result  = f"{v:.2f}{STORAGE_UNITS[i]}"
    return result

def convertToKB(cmc: str, value: str) -> int:
    i = STORAGE_UNITS.index(value[-2:])
    v = int(value[:-2])
    while(i != 1):
        pass

def getCpuUsage(previous: Process, present: Process) -> float:
    cpu_usage = float((present.getExecutionTime() - previous.getExecutionTime()) / (present.getCreationTime() - previous.getCreationTime()))
    if(cpu_usage < 0.0 or cpu_usage > 100):
        return 0.0
    return cpu_usage