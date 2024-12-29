# Class to perform graphical interface operations
# Author: Fernando Abreu e Augusto Rosa
# Date: 12/09/2024
###################################################################################################
# IMPORT
###################################################################################################
import sys
import threading
from controller.controller import Controller, buffer_general_screen_data
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QPalette
from view.header import Header
from view.general import GeneralScreen
###################################################################################################
# MACROS
###################################################################################################
TITLE: str = "Dashboard - Gerenciador de Tarefas"
WINDOW_SIZE_X: int = 1200
WINDOW_SIZE_Y: int = 700

NOT_EVENT: int = 0
HEADER_GENERAL_BUTTON_CLICK_EVENT: int = 1
HEADER_PROCESSOR_BUTTON_CLICK_EVENT: int = 2
HEADER_MEMORY_BUTTON_CLICK_EVENT: int = 3
HEADER_PROCESS_BUTTON_CLICK_EVENT: int = 4

UPDATE_TIME_SCREEN: int = 500 # ms
###################################################################################################

class View(QMainWindow):

    def __init__(self, app: QApplication):
        super().__init__()
        self.__app = app
        self.__window = QWidget()
        self.__window.setWindowTitle(TITLE)
        self.__window.setFixedSize(WINDOW_SIZE_X, WINDOW_SIZE_Y)

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

        self.__header = Header(self.__window)
        self.__header.eventClickGeneralButton(self.headerGeneralButtonClickEvent)
        self.__header.eventClickProcessorButton(self.headerProcessorButtonClickEvent)
        self.__header.eventClickMemoryButton(self.headerMemoryButtonClickEvent)
        self.__header.eventClickProcessButton(self.headerProcessButtonClickEvent)

        self.__screen = GeneralScreen(self.__app, self.__window)

        self.__header_buttons_click_event: int = NOT_EVENT

        self.__controller: Controller = None
        
        self.__timer: QTimer = QTimer()
        self.__timer.timeout.connect(self.__screen.update)
        self.__timer.setInterval(UPDATE_TIME_SCREEN)
        self.__timer.start()

        self.consumer_thread = threading.Thread(target=self.consumerData, name="Consumer", daemon=True)

    def connect(self, controller: Controller):
        self.__controller = controller

    def consumerData(self):
        while(True):
            self.__screen.setData(buffer_general_screen_data.get())
            print("View consumindo os dados...")

    def consumer(self):
        self.consumer_thread.start()

    def run(self):
        self.__window.show()
        sys.exit(self.__app.exec())

    ''' Click Event Function for Header Buttons. '''

    def headerGeneralButtonClickEvent(self):
        print("General")
        self.__header_buttons_click_event = HEADER_GENERAL_BUTTON_CLICK_EVENT
        # Here the context change will happen
    
    def headerProcessorButtonClickEvent(self):
        self.__header_buttons_click_event = HEADER_PROCESSOR_BUTTON_CLICK_EVENT
        print("Processor")
        # Here the context change will happen
    def headerMemoryButtonClickEvent(self):
        self.__header_buttons_click_event = HEADER_MEMORY_BUTTON_CLICK_EVENT
        print("Memory")
        # Here the context change will happen

    def headerProcessButtonClickEvent(self):
        self.__header_buttons_click_event = HEADER_PROCESS_BUTTON_CLICK_EVENT
        # Here the context change will happen

# end of the class View
