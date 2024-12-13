# Class to perform graphical interface oeprations
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
from view.screen import Screen
from view.general import GeneralScreen
from PyQt6 import QtCore
from PyQt6 import QtGui
import time
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
###################################################################################################

class Communicate(QtCore.QObject):
    update_signal = QtCore.pyqtSignal(object)

class View(QMainWindow):
    __app: QApplication = None

    __window: QWidget = None 

    __palette: QPalette = None

    __header: Header = None

    __screen: Screen = None

    __select_header_button: int = None

    __header_buttons_click_event: int = NOT_EVENT

    __controller : Controller = None

    __data: list = None

    __timer: QTimer = None

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

        self.__screen = GeneralScreen(self.__app, self.__window)

        self.__header_buttons_click_event: int = NOT_EVENT

        self.__controller: Controller = None

        self.__data = None

        self.__dataGeneral = None

        self.communicate = Communicate()
        self.communicate.update_signal.connect(self.update_gui)

        '''
        self.__timer_data = QTimer()
        self.__timer_data.timeout.connect(self.updateData)
        self.__timer_data.setInterval(4000)
        self.__timer_data.start()

        self.__timer: QTimer = QTimer()
        self.__timer.timeout.connect(lambda: self.__screen.update(self.__data))
        self.__timer.setInterval(4000)
        self.__timer.start()
        '''


    def update_gui(self, data):
        self.__screen.update(data)

    def updateData(self):
        if self.__controller is not None:
            self.__data = self.__controller.dataRequestFromTheGeneralScreen2()


    def connect(self, controller: Controller):
        self.__controller = controller
        consumer_thread = threading.Thread(target=self.consumerDataGeneralScreen)
        consumer_thread.daemon = True
        consumer_thread.start() # O consumidor espera o dado do buffer
        self.__controller.dataRequestFromTheGeneralScreen() # faz a requisição de dados e criar a thread de Produtor
        #consumer_thread.join() # libera o quando as duas threads tiverem sido terminadas
        #self.__screen.update(self.__data)

    def consumerDataGeneralScreen(self) -> None:
        while True:
            if not buffer_general_screen_data.empty():
                self.__data = buffer_general_screen_data.get()
                print(self.__data[0])
                print("View consumindo os dados...")
            else:
                time.sleep(0.1)

    def run(self):
        self.__window.show()
        sys.exit(self.__app.exec())

    ''' Click Event Function for Header Buttons. '''

    def addEventClickGeneralButton(self, func):
        self.__header.eventClickGeneralButton(func)


    def headerGeneralButtonClickEvent(self):
        print("Botão Geral Apertado")
        self.__app.processEvents()
        if self.__header_buttons_click_event != HEADER_GENERAL_BUTTON_CLICK_EVENT:
            self.__header_buttons_click_event = HEADER_GENERAL_BUTTON_CLICK_EVENT
            del self.__screen
            self.__screen = GeneralScreen(self.__app, self.__window)
        consumer_thread = threading.Thread(target=self.consumerDataGeneralScreen)
        consumer_thread.start() # O consumidor espera o dado do buffer
        self.__controller.dataRequestFromTheGeneralScreen() # faz a requisição de dados e criar a thread de Produtor
        #consumer_thread.join() # libera o quando as duas threads tiverem sido terminadas
        self.__screen.update(self.__data)
        print("Botão Geral Apertado")
    def headerGeneralButtonClickEvent2(self):
        self.__screen.update(self.__controller.dataRequestFromTheGeneralScreen2())


    
    def headerProcessorButtonClickEvent(self):
        self.__header_buttons_click_event = HEADER_PROCESSOR_BUTTON_CLICK_EVENT
        print("Processor")
    def headerMemoryButtonClickEvent(self):
        self.__header_buttons_click_event = HEADER_MEMORY_BUTTON_CLICK_EVENT
        print("Memory")
    def updateDataFromModel(self):
        self.__controller.updateDataFromModel()

    def consume_data(self, data):
        self.__screen.update(data)
# end of the class View

if __name__=='__main__':
    view: View = View()
    view.run()
