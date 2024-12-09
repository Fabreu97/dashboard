# Class to group information about a metric in relation to time
# Author: Fernando Abreu
# Date: 11/25/2024
###################################################################################################
# IMPORT
import time
###################################################################################################
# MACROS
# COOD
###################################################################################################
class TimeMetric:
    def __init__(self, metric: float | int, time: float = time.time()) -> None:
        self.__metric: float = metric
        self.__time: float = time
    def setMetric(self, metric: float) -> None:
        self.__metric = metric
    def getMetric(self) -> float:
        return self.__metric
    def setTime(self, time: float) -> None:
        self.__time = time
    def getTime(self) -> float:
        return self.__time
    def getInfo(self) -> list:
        return [self.__time, self.__metric]
# end of the class TimeMetric