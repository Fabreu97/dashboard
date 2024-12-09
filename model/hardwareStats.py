# Class to group information of Hardware
# Authors: Fernando Abreu e Augusto Rosa
# Date: 12/06/2024
###################################################################################################
# IMPORT
import os
import time
from TimeMetric import TimeMetric
from process import convertToLargestUnit
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter
###################################################################################################
# MACROS
READ: str = "r"
LIMIT_METRIC: int = 60
CLOCK_TICK: int = os.sysconf("SC_CLK_TCK")
STANDARD_TIME_JIFFY: float = float(1/CLOCK_TICK)
CPU_USAGE_STATS: tuple = ('id_processor', 'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal', 'guest', 'guest_nice')
###################################################################################################
# INFORMATION
##
# nomes que contem '*' no final quer dizer que foi dado por um dos autores.
# CLK_TCK   : é a quantidade de "tics" do relógio do sistema por segundo
#   clk_tck = os.sysconf("SC_CLK_TCK") // equivalente a uma chamada de systema na biblioteca C para sistemas POSIX
# jiffy     : unidade de tempo utilizada internamente pelo kernel Linux.
#   jiffy = 1/CLK_TCK
##
# /proc/uptime
#   Primeiro valor(system_uptime*)  : tempo total de atividade do sistema operacional desde que foi iniciado
#   Segundo valor(idle__time*)      : Somatório do tempo de inatividade de cada núcleo do processador desde que o sistema operacional foi inicializado
##
# /proc/stat
#   cpuX: 10 valores int na mesma linhacomo unidade jiffies
#       X: numero do processador
#       1.° user    = tempo gasto em modo usuário
#       2.° nice    = tempo gasto em modo usuário em baixa prioridade
#       3.° system  = tempo gasto em modo sistema
#       4.° idle    = tempo gasto em tarefas inativas
#       5.° iowait  = tempo de espera pela I/O para completar(ESSE VALOR NÃO É CONFIÁVEL)
#       6.° irq     = interrupções por serviços de tempo
#       7.° softirq = interrupções soft por serviços de tempo
#       8.° steal   = tempo roubado(tempo gasto em outros sistemas operacionais ao executar em um ambiente virtualizado)
#       9.° guest   = tempo gasto executando uma CPU virtual por um sistema operacional convidado sob o controle do Kernel Linux
#       10.° guest_nice = tempo gasto executando uma CPU virtual em baixa prioridade.
#   btime: tempo inicialização, em segundos, desde o Epoch, 1970-01-01
###################################################################################################
class HardwareStats:
    def __init__(self, limit: int = LIMIT_METRIC):
        self.__jiffy: float = STANDARD_TIME_JIFFY
        self.__memory_info: dict = {}
        self.__processors_info: list = []
        self.__cpu_usage_total: list = []
        self.__cpu_usage_per_processor: list = []
        self.__total_time_per_processor: list = []
        self.__idle_time_per_processor: list = []
        self.__cpu_usage_stats_per_processor: list = []
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
        
        path = "/proc/stat"
        try:
            with open(path, READ) as file:
                i: int = 0
                for line in file:
                    data: list = line.strip().split()
                    stats: dict = {}
                    total_time: float = 0.0
                    idle_time: float = self.__jiffy * (int(data[4]) + int(data[5]) + int(data[6]) + int(data[7]))
                    cpu_ = data[0][:3]
                    if cpu_ == "cpu":
                        stats[CPU_USAGE_STATS[0]] = i
                        for j in range(1, len(CPU_USAGE_STATS)):
                            total_time += self.__jiffy * int(data[j])
                            stats[CPU_USAGE_STATS[j]] = self.__jiffy * int(data[j])
                        self.__cpu_usage_stats_per_processor.append(stats)
                        self.__total_time_per_processor.append(total_time)
                        self.__idle_time_per_processor.append(idle_time)
                        self.__cpu_usage_per_processor.append([])
                    else:
                        break
                    i += 1
        except Exception as e:
            print(f"ERROR initial Hardware Stats in the path {path}: {e}")
    def updateStats(self) -> None:
        # update info CPU Total
        path = "/proc/uptime"
        try:
            with open(path, "r") as file:
                info = file.readline().strip().split()
                system_uptime = float(info[0])
                idle_time = float(info[1])
                su = system_uptime - self.__system_uptime
                it = idle_time - self.__idle_time
                time_total = len(self.__processors_info)*su
            if len(self.__cpu_usage_total) == self.__limit_metric:
                del self.__cpu_usage_total[0]
            cpu_usage_in_percentage: float = (time_total - it) / time_total
            if cpu_usage_in_percentage < 0.0:
                cpu_usage_in_percentage = 0.0
            time_metric: TimeMetric = TimeMetric(cpu_usage_in_percentage)
            self.__cpu_usage_total.append(time_metric)
            self.__system_uptime = system_uptime
            self.__idle_time = idle_time
        except Exception as e:
            print(f"ERROR updateStats of Hardware Stats in the path {path}: {e}")
        # Update Info Memory
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
            time_metric: TimeMetric = TimeMetric(value)
            self.__memory_usage.append(time_metric)
        except Exception as e:
            print(f"ERROR updateStats of Hardware Stats in the path {path}: {e}")
    
        # update CPU per processor
        path = "/proc/stat"
        try:
            with open(path, READ) as file:
                i: int = 0
                for line in file:
                    data: list = line.strip().split()
                    cpu_ = data[0][:3]
                    if cpu_ == "cpu":
                        total_time = 0.0
                        idle_time = self.__jiffy * (int(data[4]) + int(data[5]))
                        for j in range(1, len(CPU_USAGE_STATS)):
                            total_time += self.__jiffy * int(data[j])
                            self.__cpu_usage_stats_per_processor[i][CPU_USAGE_STATS[j]] = self.__jiffy * int(data[j])
                        cpu_usage_per_processor = ((total_time - self.__total_time_per_processor[i]) - (idle_time - self.__idle_time_per_processor[i])) / (total_time - self.__total_time_per_processor[i])
                        if len(self.__cpu_usage_per_processor[i]) == self.__limit_metric:
                            del self.__cpu_usage_per_processor[i][0]
                        time_metric: TimeMetric = TimeMetric(cpu_usage_per_processor)
                        self.__cpu_usage_per_processor[i].append(time_metric)
                        self.__total_time_per_processor[i] = total_time
                        self.__idle_time_per_processor[i] = idle_time
                    else:
                        break
                    i += 1
        except Exception as e:
            print(f"ERROR updateStats of Hardware Stats in the path {path}: {e}")
    def getMemoryInfo(self) -> dict:
        return self.__memory_info
    def getProcessorsInfo(self) -> list:
        return self.__processors_info
    def getCpuUsageCurrent(self) -> str:
        # return f"{self.__cpu_usage_total[-1]*100:.2f}%"
        return f"{self.__cpu_usage_total[-1].getMetric()*100:.2f}%"
    def getMemoryUsageCurrent(self) -> str:
        return f"{convertToLargestUnit('KB',self.__memory_usage[-1].getMetric())}"
    def getCpuUsage(self) -> list:
        ans: list = []
        time: list = []
        metric: list = []
        for i in self.__cpu_usage_total:
            time.append(i.getTime())
            metric.append(i.getMetric())
        ans.append(time)
        ans.append(metric)
        return ans
    def getMemoryUsage(self) -> list:
        return self.__memory_usage
    def setLimitMetric(self, limit: int) -> None:
        self.__limit_metric = limit
    def getLimitMetric(self) -> int:
        return self.__limit_metric
    def getCpuUsageStatsPerProcessor(self) -> list:
        return self.__cpu_usage_stats_per_processor
    def getCpuUsagePerProcessorCurrent(self) -> list:
        ans: list = []
        for i in range(1,len(self.__cpu_usage_per_processor)):
            ans.append(self.__cpu_usage_per_processor[i][-1].getMetric())
        return ans 
    def getCpuUsagePerProcessor(self) -> list:
        return self.__cpu_usage_per_processor
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
        time.sleep(1.0)
        s = time.time()
        stats.updateStats()
        e = time.time()
        cpu_usage = stats.getCpuUsage()
        cpu_usage_per_processor: list = stats.getCpuUsagePerProcessor()
        #cpu_usage = [i * 100 for i in cpu_usage]
        plt.clf()
        plt.plot(cpu_usage[0], cpu_usage[1])
        plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
        plt.title("CPU Usage in %")
        plt.xlabel("time")
        plt.ylabel("CPU USAGE %")
        plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))
        plt.draw()
        plt.show()
        plt.pause(0.1)
            
        print(f"Elapsed Time to updateStats: {float(e-s)*1000: .2f}ms")
        print(f"CPU usage:{stats.getCpuUsageCurrent()}")
        for i,p in enumerate(cpu_usage_per_processor):
            print(f"CPU{i} usage:{p[-1]*100:.1f}%")
        print(f"Memory usage: {stats.getMemoryUsageCurrent()}")
        # print(stats.getMemoryInfo()["MemTotal"])
        print(f"Memory Total: {convertToLargestUnit('KB', int(stats.getMemoryInfo()['MemTotal']))}")
        print("===========================================")
    plt.ioff()
    plt.show()
