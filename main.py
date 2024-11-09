from model import getListProcess, VProcess
import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel

def main():
    app = QApplication(sys.argv)

    # Criar a janela principal
    window = QWidget()
    window.setWindowTitle("Dashboard - Gerenciador de Tarefas")
    window.setFixedSize(1000, 600)

    # Layout principal
    layout = QVBoxLayout()

    # Criar o QTableWidget (tabela)
    lprocess = getListProcess()
    table = QTableWidget()
    table.setRowCount(len(lprocess))  # Número de linhas
    table.setColumnCount(2)  # Número de colunas
    table.setHorizontalHeaderLabels(["PID", "Name"])
    table.setFixedSize(500,300)
    table.setGeometry(30,200, 960, 250)
    table.setColumnWidth(0,100)
    table.setColumnWidth(1,300)
    for i,p in enumerate(lprocess):
            j = 0
            table.setItem(i,j, QTableWidgetItem(p.getId()))
            j += 1
            table.setItem(i,j, QTableWidgetItem(p.getName()))
    # Adicionar itens à tabela (Nome, Valor, Descrição)
    def update() -> None:
        start_time = time.time()
        lprocess = getListProcess()
        half_time = time.time()
        table.setRowCount(len(lprocess))  # Número de linhas
        for i,p in enumerate(lprocess):
            j = 0
            table.setItem(i,j, QTableWidgetItem(p.getId()))
            j += 1
            table.setItem(i,j, QTableWidgetItem(p.getName()))
        end_time = time.time()
        print(f"T1: {(half_time - start_time):2f}")
        print(f"T2: {end_time - start_time:2f}\n")
    # Função para mostrar o item selecionado
    def show_selected_item():
        selected_item = table.currentItem()
        if selected_item:
            row = table.currentRow()
            col = table.currentColumn()
            print(f"Item selecionado: {table.item(row, 0).text()} - {table.item(row, 1).text()}")
        else:
            print("Nenhum item selecionado")
    def clickedevent():
        update()
    # Botão para mostrar item selecionado
    button = QPushButton("Atualizar", window)
    button.clicked.connect(clickedevent)
    button.setGeometry(10,480, 100,40)
    button.setStyleSheet('color: White; background-color: Blue; font-size:15px; font-family: Roboto')
    # Adicionar widgets ao layout
    layout.addWidget(table)
    #layout.addWidget(button)
    #layout.addWidget(b)
    button.hide()
    button.show()
    # Definir o layout da janela principal
    window.setLayout(layout)

    # Exibir a janela
    window.show()

    # Iniciar o loop da aplicação
    sys.exit(app.exec())

# Executar a função principal
if __name__ == "__main__":
    main()
