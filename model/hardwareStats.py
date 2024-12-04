# Class to group information of Hardware
# Author: Fernando Abreu e Augusto Rosa
# Date: 11/25/2024
###################################################################################################
# IMPORT
import time
from TimeMetric import TimeMetric
from process import convertToLargestUnit
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter
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
                    value: int = line[index+1:].strip().split()[0]
                    #self.__memory_info[key] = convertToLargestUnit('KB',int(''.join(filter(str.isdigit, line))))
                    self.__memory_info[key] = value
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
                time_total = len(self.__processors_info)*su
            if len(self.__cpu_usage) == self.__limit_metric:
                del self.__cpu_usage[0]
            self.__cpu_usage.append((time_total - it) / time_total)
            self.__system_uptime = system_uptime
            self.__idle_time = idle_time
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
            if len(self.__memory_usage) == self.__limit_metric:
                del self.__memory_usage[0]
            value = int(self.__memory_info["MemTotal"]) - value
            self.__memory_usage.append(value)
        except Exception as e:
            print(f"ERROR updateStats of Hardware Stats in the path {path}: {e}")
    def getMemoryInfo(self) -> dict:
        return self.__memory_info
    def getProcessorsInfo(self) -> list:
        return self.__processors_info
    def getCpuUsageCurrent(self) -> str:
        return f"{self.__cpu_usage[-1]*100:.2f}%"
    def getMemoryUsageCurrent(self) -> str:
        return f"{convertToLargestUnit('KB',self.__memory_usage[-1])}"
    def getCpuUsage(self) -> list:
        return self.__cpu_usage
    def getMemoryUsage(self) -> list:
        return self.__memory_usage
    def setLimitMetric(self, limit: int) -> None:
        self.__limit_metric = limit
    def getLimitMetric(self) -> int:
        return self.__limit_metric
# end of the class HardwareStats

# Test of class
if __name__=='__main__':
    stats: HardwareStats = HardwareStats()
    # Ativa o modo interativo
    plt.ion()
    plt.title("CPU Usage in %")
    plt.xlabel("time")
    plt.ylabel("CPU USAGE %")
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))
    while(True):
        start = time.time()
        end = start
        while((end - start) < 1.0):
            end = time.time()
        s = time.time()
        stats.updateStats()
        e = time.time()
        cpu_usage = stats.getCpuUsage()
        x = range(0,len(cpu_usage))
        #cpu_usage = [i * 100 for i in cpu_usage]
        plt.clf()
        plt.plot(x, cpu_usage)
        plt.grid(True, color='darkBlue', linestyle='--', linewidth=0.5)
        plt.title("CPU Usage in %")
        plt.xlabel("time")
        plt.ylabel("CPU USAGE %")
        plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))
        plt.draw()
        plt.show()
        plt.pause(0.1)
            
        print(f"Elapsed Time to updateStats: {float(e-s)*1000: .2f}ms")
        print(f"CPU usage:{stats.getCpuUsageCurrent()}")
        print(f"Memory usage: {stats.getMemoryUsageCurrent()}")
        # print(stats.getMemoryInfo()["MemTotal"])
        print(f"Memory Total: {convertToLargestUnit('KB', int(stats.getMemoryInfo()['MemTotal']))}")
        print("===========================================")
    plt.ioff()
    plt.show()