from model import getInfoProcess,  VProcess
import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt6.QtGui import QColor, QPalette
def main():
    app = QApplication(sys.argv)

    # Criar a janela principal
    window = QWidget()
    window.setWindowTitle("Dashboard - Gerenciador de Tarefas")
    window.setFixedSize(1000, 600)

    # Criar um QPalette para configurar o modo escuro
    dark_palette = QPalette()

    # Definindo as cores do modo escuro
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))  # Cor de fundo da janela
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))  # Cor do texto da janela
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(64, 64, 64))  # Cor do botão
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))  # Cor do texto do botão
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))  # Cor de fundo de caixas de entrada (line edit)
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))  # Cor alternada de fundo
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))  # Cor do texto
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(200, 200, 255))  # Cor do destaque de seleção
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))  # Cor do texto destacado

    # Aplica o QPalette ao aplicativo
    app.setPalette(dark_palette)

    # Layout principal
    layout = QVBoxLayout()

    # Criar o QTableWidget (tabela)
    start_time = time.time()
    lprocess = getInfoProcess()
    half_time = time.time()
    table = QTableWidget()
    table.setRowCount(len(lprocess))  # Número de linhas
    table.setColumnCount(6)  # Número de colunas
    table.setHorizontalHeaderLabels(["PID", "COMMAND", "STATE", "PARENT", "START_TIME", "VSIZE"])
    table.setFixedSize(960,300)
    table.setGeometry(30,200, 960, 250)
    table.setColumnWidth(0,100)
    table.setColumnWidth(1,360)
    table.setColumnWidth(2,100)
    table.setColumnWidth(3,100)
    table.setColumnWidth(4,100)
    table.setColumnWidth(5,100)
    for i,p in enumerate(lprocess):
        list_info = p.getInfo()
        for j,l in enumerate(list_info):
            table.setItem(i,j, QTableWidgetItem(str(l)))
    end_time = time.time()
    print(f"T1: {(half_time - start_time):2f}")
    print(f"T2: {end_time - half_time:2f}\n")
    # Adicionar itens à tabela (Nome, Valor, Descrição)
    def update() -> None:
        start_time = time.time()
        lprocess = getInfoProcess()
        half_time = time.time()
        table.setRowCount(len(lprocess))  # Número de linhas
        for i,p in enumerate(lprocess):
            list_info = p.getInfo()
            for j,l in enumerate(list_info):
                table.setItem(i,j, QTableWidgetItem(str(l)))
        end_time = time.time()
        print(f"T1: {(half_time - start_time):2f}")
        print(f"T2: {end_time - half_time:2f}\n")
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
