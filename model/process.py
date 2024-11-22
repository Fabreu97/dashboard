# Classe para agrupar as informações de um processo.

STORAGE_UNITS = ("B", "KB", "MB", "GB", "TB")

# TODO: find a way to find uot how much time a process consumes on the Process class

class Process:
    def __init__(self, PID : int, command: str, state: str, PPID: int, RSS: int) -> None:
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
    def getPId(self) -> int:
        return self.id
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
