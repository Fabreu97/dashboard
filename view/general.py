# Class for application General Screen
# Author: Fernando Abreu e Augusto Rosa
# Date: 12/10/2024
###################################################################################################
# IMPORT
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QLabel
from view.screen import Screen
###################################################################################################
# MACROS
## TABLE
LABELS_TABLE = ["PID", "NAME", "STATE", "PPID", "MEMORY", "CPU USAGE(%)"]
POSITION_TABLE_X = 20
POSITION_TABLE_Y = 200
SIZE_TABLE_X = 900
SIZE_TABLE_Y = 300
## DATA
SIZE_OF_THE_PROCESS_LIST  = 0
PROCESS_LIST  = 1
CPU_USAGE = 2
MEMORY_USAGE  = 3
MEMORY_TOTAL  = 4
TOTAL_THREADS = 5
NUMBER_OF_RUNNING_PROCESSES = 6
NUMBER_OF_SLEEPING_PROCESSES = 7
NUMBER_OF_ZUMBI_PROCESSES = 8
NUMBER_OF_STOPPED_PROCESSES = 9
NUMBER_OF_IDLE_PROCESSES = 10
NUMBER_OF_PROCESSING_CORES = 11
VERSION_OS = 12
## LABEL
STYLE_SHEET = "font-size: 16px; font-weight: bold;"
INITIAL_LINE_X = 20
INITIAL_LINE_Y = 45
VERTICAL_SPACE = 30

###################################################################################################

class GeneralScreen(Screen):
    def __init__(self, app: QApplication, window: QWidget, data = None):
        super().__init__()
        self.__app = app
        self.__window = window

        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(20, POSITION_TABLE_Y + 30, 20, 10)

        self.__table = QTableWidget()
        self.__table.setColumnCount(len(LABELS_TABLE))
        self.__table.setHorizontalHeaderLabels(LABELS_TABLE)
        self.__table.setGeometry(POSITION_TABLE_X, POSITION_TABLE_Y, SIZE_TABLE_X, SIZE_TABLE_Y)
        self.__table.setColumnWidth(0,50)
        self.__table.setColumnWidth(1,450)
        self.__table.setColumnWidth(2,200)
        self.__table.setColumnWidth(3,50)
        self.__table.setColumnWidth(4,100)
        self.__table.setColumnWidth(5,125)
        if data is not None:
            self.__table.setRowCount(data[SIZE_OF_THE_PROCESS_LIST])  # Número de linhas
            for i, process in enumerate(data[PROCESS_LIST]):
                for j, info in enumerate(process):
                    self.__table.setItem(i,j, QTableWidgetItem(str(info)))

        self.__line01 = QLabel("CPU Usage:  undefined", parent=self.__window)
        self.__line01.move(INITIAL_LINE_X, INITIAL_LINE_Y)
        self.__line01.setStyleSheet(STYLE_SHEET)
        self.__line01.adjustSize()

        self.__line02 = QLabel(". . .", parent=self.__window)
        self.__line02.move(INITIAL_LINE_X, INITIAL_LINE_Y + 1*VERTICAL_SPACE)
        self.__line02.setStyleSheet(STYLE_SHEET)
        self.__line02.adjustSize()

        self.__line03 = QLabel("Memory Total:  undefined", parent=self.__window)
        self.__line03.move(INITIAL_LINE_X, INITIAL_LINE_Y + 2*VERTICAL_SPACE)
        self.__line03.setStyleSheet(STYLE_SHEET)
        self.__line03.adjustSize()

        self.__line04 = QLabel("Memory Usage:  undefined", parent=self.__window)
        self.__line04.move(INITIAL_LINE_X, INITIAL_LINE_Y + 3*VERTICAL_SPACE)
        self.__line04.setStyleSheet(STYLE_SHEET)
        self.__line04.adjustSize()

        self.__line05 = QLabel("Version:  undefined", parent=self.__window)
        self.__line05.move(INITIAL_LINE_X, INITIAL_LINE_Y + 4*VERTICAL_SPACE)
        self.__line05.setStyleSheet(STYLE_SHEET + "color: #00FF00;")
        self.__line05.adjustSize()


        self.__layout.addWidget(self.__table)
        self.__window.setLayout(self.__layout)


    def update(self):
        if self._data is not None:
            self.__table.setRowCount(self._data[SIZE_OF_THE_PROCESS_LIST])  # Número de linhas
            for i, process in enumerate(self._data[PROCESS_LIST]):
                for j, info in enumerate(process):
                    self.__table.setItem(i,j, QTableWidgetItem(str(info)))
            self.__line01.setText("CPU Usage:  " + self._data[CPU_USAGE] + "                   Total number of processing cores:  " + str(self._data[NUMBER_OF_PROCESSING_CORES]))
            self.__line01.adjustSize()
            
            self.__line02.setText("Tasks:  " + str(self._data[SIZE_OF_THE_PROCESS_LIST]) + "                   Running Tasks:  " + str(self._data[NUMBER_OF_RUNNING_PROCESSES]) + "                   Sleeping Tasks:  " + str(self._data[NUMBER_OF_SLEEPING_PROCESSES]) + "                   Stopped Tasks:  " + str(self._data[NUMBER_OF_STOPPED_PROCESSES]) + "                   Idle Tasks:  " + str(self._data[NUMBER_OF_IDLE_PROCESSES]) + "                   Zumbi Tasks:  " + str(self._data[NUMBER_OF_ZUMBI_PROCESSES]))
            self.__line02.adjustSize()
            
            self.__line03.setText("Memory Total:  " + self._data[MEMORY_TOTAL] + "                   Memory Usage:  " + str(self._data[MEMORY_USAGE]))
            self.__line03.adjustSize()

            self.__line04.setText("Total Threads:  " + str(self._data[TOTAL_THREADS]))
            self.__line04.adjustSize()

            self.__line05.setText("Version:  " + self._data[VERSION_OS])
            self.__line05.adjustSize()
            
            self._data = None

        # self.__window.show()
# end of the class General Screen
