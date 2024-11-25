# Class to group the information of a process.
# Author: Fernando Abreu
# Date: 11/23/2024
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
#   PPID: Processo pai
#   RSS: uso de memoria residente(stats é dado por páginas e status é dado em KB)
#   wchan: canal de espera, mostra o que o processo esta aguardando
#   cmdline: linha de comando da execução do processo
#   threads: Número de threads no processo
###################################################################################################
class Process:
    def __init__(self, PID : int, command: str, state: str, PPID: int, RSS: int):
        self.PID = PID
        self.command = command
        if (state=='R'):
            self.state = "Execução"
        elif(state == 'S' or state == 'D'):
            self.state = "Aguardando"
        elif(state == 'Z'):
            self.state = "Zumbi"
        elif(state == 'T'):
            self.state = "Paralisado"
        elif(state == 'I'):
            self.state = "Inativo"
        else:
            self.state = "Desconhecido"
        self.PPID = PPID
        self.RSS = RSS
        self.memory = convertToLargestUnit('KB', RSS)
        self.children: list = []
        self.wchan = ""
        self.cmdline = ""
        self.threads = 0
    def getPID(self) -> int:
        return self.PID
    def getCommand(self) -> str:
        return self.command
    def getState(self) -> str:
        return self.state
    def getParent(self) -> int:
        return self.PPID
    def getRSS(self) -> int:
        return self.RSS
    def getMemory(self) -> str:
        return self.memory
    def getInfo(self) -> list:
        return [self.PID, self.command, self.state, self.PPID, self.memory]
    def addProcessChildren(self, process) -> None:
        self.children.append(process)
    def setWaitChannel(self, wchan: str) -> None:
        self.wchan = wchan
    def getWaitChannel(self) -> str:
        return self.wchan
    def setCommandLine(self, cmdline: str) -> None:
        self.cmdline = cmdline
    def getCommandLine(self) -> str:
        return self.cmdline
    def setThreads(self, threads: int) -> None:
        self.threads = threads
    def getThreads(self) -> int:
        return self.threads
# end of the class Process

def convertToLargestUnit(cmc: str, value: int) -> str:
    result: str = ""
    try:
        i = STORAGE_UNITS.index(cmc)
    except ValueError:
        print(f"Elemento não encontrado: {cmc}")
    v = value
    while(float(v/1024) >= 1.0):
        v = v/1024
        i += 1
    result  = f"{v:.2f}{STORAGE_UNITS[i]}"
    return result
