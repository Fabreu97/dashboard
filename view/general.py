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
POSITION_TABLE_X: int = 20
POSITION_TABLE_Y: int = 200
SIZE_TABLE_X: int = 900
SIZE_TABLE_Y: int = 300
## DATA
SIZE_OF_THE_PROCESS_LIST: int = 0
PROCESS_LIST: int = 1
CPU_USAGE: int = 2
MEMORY_USAGE: int = 3
MEMORY_TOTAL: int = 4
TOTAL_THREADS: int = 5
## LABEL
STYLE_SHEET: str = "font-size: 16px;"
INITIAL_LINE_X: int  = 20
INITIAL_LINE_Y: int = 45
VERTICAL_SPACE: int = 30

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

        self.__text_cpu = QLabel("CPU Usage: undefined", parent=self.__window)
        self.__text_cpu.move(INITIAL_LINE_X, INITIAL_LINE_Y)
        self.__text_cpu.setStyleSheet(STYLE_SHEET)
        self.__text_cpu.adjustSize()

        self.__text_memory_total = QLabel("Memory Total: undefined", parent=self.__window)
        self.__text_memory_total.move(INITIAL_LINE_X, INITIAL_LINE_Y + 1*VERTICAL_SPACE)
        self.__text_memory_total.setStyleSheet(STYLE_SHEET)
        self.__text_memory_total.adjustSize()

        self.__text_memory_usage = QLabel("Memory Usage: undefined", parent=self.__window)
        self.__text_memory_usage.move(INITIAL_LINE_X, INITIAL_LINE_Y + 2*VERTICAL_SPACE)
        self.__text_memory_usage.setStyleSheet(STYLE_SHEET)
        self.__text_memory_usage.adjustSize()

        self.__text_total_threads = QLabel("Total Threads: undefined", parent=self.__window)
        self.__text_total_threads.move(INITIAL_LINE_X, INITIAL_LINE_Y + 3*VERTICAL_SPACE)
        self.__text_total_threads.setStyleSheet(STYLE_SHEET)
        self.__text_total_threads.adjustSize()

        self.__layout.addWidget(self.__table)
        self.__window.setLayout(self.__layout)


    def update(self, data):
        if data is not None:
            self.__table.setRowCount(data[SIZE_OF_THE_PROCESS_LIST])  # Número de linhas
            for i, process in enumerate(data[PROCESS_LIST]):
                for j, info in enumerate(process):
                    self.__table.setItem(i,j, QTableWidgetItem(str(info)))
        self.__text_cpu.setText("CPU Usage: " + data[CPU_USAGE])
        self.__text_memory_total.setText("Memory Total: " + data[MEMORY_TOTAL])
        self.__text_memory_usage.setText("Memory Usage: " + data[MEMORY_USAGE])
        self.__text_total_threads.setText("Total Threads: " + str(data[TOTAL_THREADS]))

        # self.__window.show()
# end of the class General Screen
