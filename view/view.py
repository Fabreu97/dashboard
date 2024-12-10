# Class to perform graphical interface oeprations
# Author: Fernando Abreu e Augusto Rosa
# Date: 12/09/2024
###################################################################################################
# IMPORT
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QColor, QPalette
from header import Header
from screen import Screen
from general import GeneralScreen
###################################################################################################
# MACROS
TITLE: str = "Dashboard - Gerenciador de Tarefas"
WINDOW_SIZE_X: int = 1200
WINDOW_SIZE_Y: int = 700
###################################################################################################

class View(QMainWindow):
    def __init__(self):
        
        __app: QApplication = None

        __window: QWidget = None 

        __palette: QPalette = None

        __header: Header = None

        __screen: Screen = None

        __select_header_button: int = None

        super().__init__
        self.__app = QApplication(sys.argv)

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
        self.__screen = GeneralScreen(self.__window)

    def update(self, data):
        self.__screen.update(data)
    def run(self):
        self.__window.show()
        sys.exit(self.__app.exec())
# end of the class View

if __name__=='__main__':
    view: View = View()
    view.run()