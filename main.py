import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
import threading
from view.view import View
from model.model import Model
from controller.controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Criando as instancias da aplicação
    view = View(app)
    model = Model()
    controller = Controller()

    # Fazendo configurações iniciais...
    # P.S.: A ordem importa das conexões.
    controller.connect(model=model)
    view.connect(controller=controller)

    def eventclickGeneralButton():
        view.headerGeneralButtonClickEvent2()
    view.addEventClickGeneralButton(eventclickGeneralButton)

    # Executando
    '''
        Executando a Thread de atualização dos dados do Model em cada 5s
    '''

    controller.updateDataFromModel() 


    '''
        Executando, de forma automatizada pela biblioteca PyQt6, a aplicação.
        P.S.: O loop de execução do programa esta sendo executado nos bastidores pela encapsulamento e automatização do PyQt6
    '''

    view.run()

    # The End