import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

from view import View
from model import Model
from controller import Controller


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Criando as instancias da aplicação do padrão MVC(Model-View-Controller)
    view = View(app)
    model = Model()
    controller = Controller()

    # Fazendo configurações iniciais...
    # P.S.: A ordem importa das conexões.
    controller.connect(model=model)
    view.connect(controller=controller)

    # Executando
    '''
        Executando as Thread de atualização dos dados, de envio dos dados(Produtor) e de recebimento dos dados(Consumer)
    '''

    controller.updateDataFromModel()
    controller.dataRequestFromTheGeneralScreen()
    view.consumer()


    '''
        Executando, de forma automatizada pela biblioteca PyQt6, a aplicação.
        P.S.: O loop de execução do programa esta sendo executado nos bastidores pelo encapsulamento e automatização do PyQt6
    '''

    view.run()

    # The End