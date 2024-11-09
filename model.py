# Model : camada de armazenamento e manipulação de dados
import os

proc = '/proc'

# ID : int
# name : str
class VProcess:
    def __init__(self, id : int, name: str):
        self.id = id
        self.name = name
    def getId(self) -> int:
        return self.id
    def getName(self) -> str:
        return self.name
    def getInfo(self) -> None:
        print(f"PID: {self.id}\nName: {self.name}\n")

def findPIDs() -> list:
    pid = []
    if os.path.exists(proc):
        dir_list = os.listdir(proc)
        for name_dir in dir_list:
            if name_dir.isdigit():
                pid.append(name_dir)
    return pid

def findName(pid : int) -> str | None:
    path = f"{proc}/{pid}"
    if os.path.exists(path):
        with open(f"{path}/comm", "r") as file:
            return file.readline().strip()
    return None

def getListProcess() -> list:
    list_process : list = []
    pids = findPIDs()
    for pid in pids:
        list_process.append(VProcess(pid, findName(pid)))
    return list_process