# Class to group a list of processes over time.
# Author: Fernando Abreu
# Date: 11/23/2024
###################################################################################################
# IMPORT
from processList import ProcessList
###################################################################################################
# MACROS
SIZE_LIMIT: int = 60
###################################################################################################
class ProcessHistory:
    def __init__(self) -> None:
        self.history: list = []
        self.sizeLimit: int = SIZE_LIMIT
    def getInfo(self):
        pass
    def addProcessList(self, old: ProcessList) -> None:
        if((self.sizeLimit + 1) > len(self.history)):
            del self.history[0] # oldest
        self.history.append(old)
    def setSizeLimit(self, limit: int) -> None:
        if (limit > 0):
            self.sizeLimit = limit
    def getSizeLimit(self) -> int:
        return self.sizeLimit
# END OF THE CLASS PROCESS_HISTORY