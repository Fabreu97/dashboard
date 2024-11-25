# Class to group information of Hardware
# Author: Fernando Abreu e Augusto Rosa
# Date: 11/25/2024
###################################################################################################
# IMPORT
import time
from TimeMetric import TimeMetric
from process import convertToLargestUnit
###################################################################################################
# MACROS
limit_metric: int = 60
###################################################################################################
# INFORMATION
# nomes que contem '*' no final quer dizer que foi dado por um dos autores.
# No arquivo /proc/uptime temos dois valores float:
# Primeiro valor(system_uptime*): tempo total de atividade do sistema operacional desde que foi iniciado
# Segundo valor(idle__time*): Somatório do tempo de inatividade de cada núcleo do processador desde que o sistema operacional foi inicializado
###################################################################################################
class HardwareStats:
    def __init__(self, limit: int = limit_metric):
        self.__memory_info: dict = {}
        self.__processors_info: list = []
        self.__cpu_usage: list = []
        self.__memory_usage: list = []
        self.__system_uptime: float = 0.0
        self.__idle_time: float = 0.0
        self.__limit_metric = limit
        path: str = "/proc/meminfo"
        try:
            with open(path, "r") as file:
                for line in file:
                    index: int = line.find(":")
                    key: str = line[:index].strip()
                    self.__memory_info[key] = convertToLargestUnit('KB',int(''.join(filter(str.isdigit, line))))
        except Exception as e:
            print(f"Error initial HardwareStats in the path {path}: {e}")
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
                                self.__processors_info.append(processor_info)
                            processor_info = {}
                        processor_info[key] = value
        except Exception as e:
            print(f"ERROR initial Hardware Stats in the path {path}: {e}")
        path = "/proc/uptime"
        try:
            with open(path, "r") as file:
                info = file.readline().strip().split()
                self.__system_uptime = float(info[0])
                self.__idle_time = float(info[1])
        except Exception as e:
            print(f"ERROR initial Hardware Stats in the path {path}: {e}")
    def updateStats(self) -> None:
        path = "/proc/uptime"
        try:
            with open(path, "r") as file:
                info = file.readline().strip().split()
                system_uptime = float(info[0])
                idle_time = float(info[1])
                su = system_uptime - self.__system_uptime
                it = idle_time - self.__idle_time
                time_total = len(self.__processors_info)
            self.__cpu_usage = (time_total * su - it) / time_total
        except Exception as e:
            print(f"ERROR updateStats of Hardware Stats in the path {path}: {e}")
        path = "/proc/meminfo"
        try:
            with open(path, "r") as file:
                for line in file:
                    index: int = line.find(":")
                    key: str = line[:index].strip()
                    if key == "MemFree":
                        value: int = int(line[index+1:].strip().split()[0])
                        break
            self.__memory_usage.append(convertToLargestUnit("KB", value))
        except Exception as e:
            pass
    def getCpuUsageCurrent(self) -> str:
        return f"{self.__cpu_usage[-1]*100}%"
    def getMemoryUsageCurrent(self) -> str:
        pass
    def getCpuUsage(self) -> list:
        return self.__cpu_usage
    def getMemoryUsage(self) -> list:
        return self.__memory_usage
    def setLimitMetric(self, limit: int) -> None:
        self.__limit_metric = limit
    def getLimitMetric(self) -> int:
        return self.__limit_metric
# end of the class HardwareStats