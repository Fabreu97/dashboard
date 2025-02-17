# Class for application General Screen
# Author: Fernando Abreu e Augusto Rosa
# Date: 16/02/2025
###################################################################################################
# IMPORT
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QTableWidget,QTableWidgetItem
from view.screen import Screen
from controller.controller import Controller
import os

#MACROS
LABELS_TABLE = ["Parameters", "Value"]
MEMORY_TAG = ["Size", "Resident", "Shared", "Text", "Lib", "Data", "Dirty Page"]

class ProcessScreen(Screen):
    def __init__(self, parent: QWidget):
        Screen.__init__(self, parent=parent)
        self.__controller: Controller = None
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        self.__seach_widget = QWidget(parent=self)
        self.__layout.addWidget(self.__seach_widget)

        self.__seach_layout = QHBoxLayout()
        self.__seach_widget.setLayout(self.__seach_layout)

        self.__line_edit = QLineEdit(parent=self.__seach_widget)
        self.__line_edit.setPlaceholderText("Digite PID pra ser pesquisado: ")

        self.search_button = QPushButton('Pesquisar', self)
        self.search_button.clicked.connect(self.on_search)

        self.__seach_layout.addWidget(self.__line_edit)
        self.__seach_layout.addWidget(self.search_button)

        self.__label = QLabel('', self)
        self.__layout.addWidget(self.__label)

        self.__text_open_files = QLabel("Numero de Arquivos abertos: ", self)
        self.__layout.addWidget(self.__text_open_files)

        self.__text_sockets_tcp = QLabel("Numero de Sockets abertos TCP: ", self)
        self.__layout.addWidget(self.__text_sockets_tcp)

        self.__text_sockets_udp = QLabel("Numero de Sockets abertos UDP: ", self)
        self.__layout.addWidget(self.__text_sockets_udp)

        self.__text_sem_mux = QLabel("Numero Semaforos e Mutex: ", self)
        self.__layout.addWidget(self.__text_sem_mux)
        
        self.__table = QTableWidget(self)
        self.__table.setColumnCount(len(LABELS_TABLE))
        self.__table.setHorizontalHeaderLabels(LABELS_TABLE)
        self.__layout.addWidget(self.__table)

        self.__table_memory = QTableWidget(self)
        self.__table_memory.setRowCount(7)
        self.__table_memory.setColumnCount(2)
        self.__table_memory.setHorizontalHeaderLabels(["Type", "Size in pages"])
        self.__layout.addWidget(self.__table_memory)
        #self.__table.setItem(i,j, QTableWidgetItem(str(info)))


    def connectController(self, controller):
        self.__controller = controller

    def on_search(self):
        query = self.__line_edit.text()
        print("teste")
        if query.isdigit():
            if not os.path.exists(f"/proc/{query}"):
                self.__label.setText(f'Esse Processo não existe: {query}')
            else:
                if(self.__controller is not None):
                    data = self.__controller.dataProcessScreen(query)
                    print(data)
                    if len(data) > 0:
                        self.__text_open_files.setText(f"Numero de Arquivos abertos: {str(data[0])}")
                        self.__text_sockets_tcp.setText(f"Numero de Sockets abertos TCP: {str(data[2])}")
                        self.__text_sockets_udp.setText(f"Numero de Sockets abertos UDP: {str(data[3])}")
                        self.__text_sem_mux.setText(f"Numero Semaforos e Mutex: {data[4]}")
                        if len(data[1]) > 0:
                            self.__table.setRowCount(len(data[1]))
                        i = 0
                        for key, value in data[1].items():
                            self.__table.setItem(i,0, QTableWidgetItem(str(key)))
                            self.__table.setItem(i,1, QTableWidgetItem(str(value)))
                            i += 1
                        if len(data[5]) > 0:
                            self.__table_memory.setRowCount(len(data[5]))
                        i = 0
                        for key, value in data[5].items():
                            self.__table_memory.setItem(i,0, QTableWidgetItem(str(key)))
                            self.__table_memory.setItem(i,1, QTableWidgetItem(str(value)))
                            i += 1
                        self.adjustSize()
        else:
            self.__label.setText(f'Não é um Número: {query}')
    def update(self):
        pass