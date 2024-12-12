# Class for application General Screen
# Author: Fernando Abreu e Augusto Rosa
# Date: 12/10/2024
###################################################################################################
# IMPORT
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from screen import Screen
###################################################################################################
# MACROS
## TABLE
LABELS_TABLE = ["PID", "NAME", "STATE", "PPID", "MEMORY", "CPU USAGE(%)"]
POSITION_TABLE_X: int = 20
POSITION_TABLE_Y: int = 200
SIZE_TABLE_X: int = 900
SIZE_TABLE_Y: int = 300
## DATA
SIZE_OF_THE_PROCESS_LIST: int = 0
PROCESS_LIST: int = 1
###################################################################################################

class GeneralScreen(Screen):
    def __init__(self, window: QWidget, data = None):
        super().__init__()
        self.__window = window
        self.__main_layout = QVBoxLayout()
        self.__main_layout.setContentsMargins(20, 30, 20, 10)
        self.__header_layout = QVBoxLayout()
        self.__header_layout.setContentsMargins(20, POSITION_TABLE_Y + 30, 20, 10)
        self.__table_layout = QVBoxLayout()
        self.__table = QTableWidget()
        self.__table.setColumnCount(len(LABELS_TABLE))
        self.__table.setHorizontalHeaderLabels(LABELS_TABLE)
        self.__table.setGeometry(POSITION_TABLE_X, POSITION_TABLE_Y, SIZE_TABLE_X, SIZE_TABLE_Y)
        self.__table.setColumnWidth(0,50)
        self.__table.setColumnWidth(1,450)
        self.__table.setColumnWidth(2,200)
        self.__table.setColumnWidth(3,50)
        self.__table.setColumnWidth(4,200)
        self.__table.setColumnWidth(5,200)
        if data is not None:
            self.__table.setRowCount(data[SIZE_OF_THE_PROCESS_LIST])  # Número de linhas
            for i, process in enumerate(data[PROCESS_LIST]):
                for j, info in enumerate(process):
                    self.__table.setItem(i,j, QTableWidgetItem(str(info)))

        #self.__table.resizeColumnsToContents()
        self.__table_layout.addWidget(self.__table)
        self.__main_layout.addLayout(self.__header_layout)
        self.__main_layout.addLayout(self.__table_layout)
        self.__window.setLayout(self.__main_layout)
    def update(self, data):
        if data is not None:
            self.__table.setRowCount(data[SIZE_OF_THE_PROCESS_LIST])  # Número de linhas
            for i, process in enumerate(data[PROCESS_LIST]):
                for j, info in enumerate(process):
                    self.__table.setItem(i,j, QTableWidgetItem(str(info)))
        print("Update General Screen")
# end of the class General Screen
