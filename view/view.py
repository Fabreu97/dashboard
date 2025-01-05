# Class to perform graphical interface operations
# Author: Fernando Abreu e Augusto Rosa
# Date: 12/09/2024
###################################################################################################
# IMPORT
###################################################################################################
import sys
import threading
from controller.controller import Controller, buffer_general_screen_data
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QStackedLayout
from PyQt6.QtCore import QTimer, QSize
from PyQt6.QtGui import QColor, QPalette
from view.header import Header
from view.general import GeneralScreen
from view.processor_details_screen import ProcessorDetailsScreen
###################################################################################################
# MACROS
###################################################################################################
TITLE: str = "Dashboard - Gerenciador de Tarefas"
MINIMUM_SIZE = QSize(1100, 600)
MAXIMUM_SIZE = QSize(1600, 1000)

NOT_EVENT: int = 0
HEADER_GENERAL_BUTTON_CLICK_EVENT: int = 1
HEADER_PROCESSOR_BUTTON_CLICK_EVENT: int = 2
HEADER_MEMORY_BUTTON_CLICK_EVENT: int = 3
HEADER_PROCESS_BUTTON_CLICK_EVENT: int = 4

UPDATE_TIME_SCREEN: int = 1000 # ms
###################################################################################################

class View():

    def __init__(self, app: QApplication):
        self.__app = app
        self.__window = QMainWindow()
        self.__window.setWindowTitle(TITLE)
        self.__window.setMinimumSize(MINIMUM_SIZE)
        self.__window.setMaximumSize(MAXIMUM_SIZE)

        self.__widget = QWidget(parent=self.__window)
        self.__main_layout = QVBoxLayout()
        self.__widget.setLayout(self.__main_layout)
        
        self.__screen_widget = QWidget(parent=self.__widget)
        self.__screen_layout = QStackedLayout()
        self.__screen_widget.setLayout(self.__screen_layout)

        self.__palette = QPalette()
        self.__palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))  # Cor de fundo da janela
        self.__palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))  # Cor do texto da janela
        self.__palette.setColor(QPalette.ColorRole.Button, QColor(64, 64, 64))  # Cor do botão
        self.__palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))  # Cor do texto do botão
        self.__palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))  # Cor de fundo de caixas de entrada (line edit)
        self.__palette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))  # Cor alternada de fundo
        self.__palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))  # Cor do texto
        self.__palette.setColor(QPalette.ColorRole.Highlight, QColor(200, 200, 255))  # Cor do destaque de seleção
        self.__palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))  # Cor do texto destacado

        # Aplica o QPalette ao aplicativo
        self.__app.setPalette(self.__palette)

        self.__header = Header(self.__widget)
        self.__header.eventClickGeneralButton(self.headerGeneralButtonClickEvent)
        self.__header.eventClickProcessorButton(self.headerProcessorButtonClickEvent)
        self.__header.eventClickMemoryButton(self.headerMemoryButtonClickEvent)
        self.__header.eventClickProcessButton(self.headerProcessButtonClickEvent)
        self.__main_layout.addWidget(self.__header)

        self.__general_screen = GeneralScreen(self.__widget)
        self.__screen_layout.addWidget(self.__general_screen)
        self.__main_layout.addWidget(self.__screen_widget)

        self.__processor_details_screen = ProcessorDetailsScreen(self.__widget)
        self.__screen_layout.addWidget(self.__processor_details_screen)
        
        self.__window.setCentralWidget(self.__widget)

        self.__header_buttons_click_event: int = NOT_EVENT

        self.__controller: Controller = None
        
        self.__timer: QTimer = QTimer()
        self.__timer.timeout.connect(self.__general_screen.update)
        self.__timer.setInterval(UPDATE_TIME_SCREEN)
        self.__timer.start()

        self.consumer_general_thread = threading.Thread(target=self.consumerData, name="Consumer General Screen", daemon=True)
        self.lock = threading.Lock()

    def connect(self, controller: Controller):
        self.__controller = controller

    def consumerData(self):
        while(True):
            self.lock.acquire()
            if(self.__general_screen is not None):
                self.__general_screen.setData(buffer_general_screen_data.get())
                print("View consumindo os dados...")
            self.lock.release()

    def consumer(self):
        self.consumer_general_thread.start()

    def run(self):
        self.__window.show()
        sys.exit(self.__app.exec())

    ''' Click Event Function for Header Buttons. '''

    def headerGeneralButtonClickEvent(self):
        print("General")
        self.__screen_layout.setCurrentIndex(0)
        # Here the context change will happen
    
    def headerProcessorButtonClickEvent(self):
        print("Processor")
        self.__screen_layout.setCurrentIndex(1)
        # Here the context change will happen
    def headerMemoryButtonClickEvent(self):
        print("Memory")
        self.__screen_layout.setCurrentIndex(1)
        # Here the context change will happen

    def headerProcessButtonClickEvent(self):
        print("Process")
        self.__screen_layout.setCurrentIndex(1)
        # Here the context change will happen

# end of the class View
