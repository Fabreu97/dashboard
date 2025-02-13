# Abstract Class for each screen
# Author: Fernando Abreu e Augusto Rosa
# Date: 12/10/2024
###################################################################################################
# IMPORT
from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QWidget
###################################################################################################
# MACROS
###################################################################################################
# CLASS
###################################################################################################
class Screen(QWidget):
    @abstractmethod
    def __init__(self, parent: QWidget):
        QWidget.__init__(self,parent=parent)
        ABC.__init__(self)
        self._data: list = None
    
    def setData(self, data: list):
        self._data = data

    @abstractmethod
    def update(self):
        pass
###################################################################################################