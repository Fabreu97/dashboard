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
class Screen(ABC):
    @abstractmethod
    def __init__(self: QWidget):
        pass
    
    @abstractmethod
    def update(self):
        pass