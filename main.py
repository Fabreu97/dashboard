from model import getInfoProcess, getInfoMem, convertUnidade, MEM_INFO_KEY
import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

N_CAMPOS_PROCESSO: int = 7 

def main():
    app = QApplication(sys.argv)

    # Criar a janela principal
    window = QWidget()
    window.setWindowTitle("Dashboard - Gerenciador de Tarefas")
    window.setFixedSize(1010, 600)

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
    infomem = getInfoMem()
    start_time = time.time()
    lprocess = getInfoProcess()
    half_time = time.time()
    table = QTableWidget()
    table.setRowCount(len(lprocess))  # Número de linhas
    table.setColumnCount(N_CAMPOS_PROCESSO)  # Número de colunas
    table.setHorizontalHeaderLabels(["PID", "COMMAND", "STATE", "PARENT", "START_TIME", "VSIZE", "MEMORY"])
    table.setFixedSize(960,300)
    table.setGeometry(20,200, 960, 300)
    table.setColumnWidth(0,50)
    table.setColumnWidth(1,300)
    table.setColumnWidth(2,100)
    table.setColumnWidth(3,100)
    table.setColumnWidth(4,100)
    table.setColumnWidth(5,100)
    table.setColumnWidth(5,100)
    for i,p in enumerate(lprocess):
        list_info = p.getInfo()
        for j,l in enumerate(list_info):
            table.setItem(i,j, QTableWidgetItem(str(l)))
    end_time = time.time()
    print(f"T1: {(half_time - start_time):.3f}")
    print(f"T2: {end_time - half_time:.3f}\n")
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
        print(f"T1: {(half_time - start_time):.3f}")
        print(f"T2: {end_time - half_time:.3f}\n")
        for i,info in enumerate(infomem):
            print(f"{MEM_INFO_KEY[i]}:{convertUnidade("KB", info):>16}")
    def sort_table(index):
        # Alterna entre ordenação crescente e decrescente
        current_sort_order = table.horizontalHeader().sortIndicatorOrder()
        if current_sort_order == Qt.SortOrder.AscendingOrder:
            table.sortItems(index, Qt.SortOrder.DescendingOrder)
        else:
            table.sortItems(index, Qt.SortOrder.AscendingOrder)
    def clickedevent():
        update()
    
    # Conectando o clique do cabeçalho à função de ordenação
    table.horizontalHeader().sectionClicked.connect(sort_table)
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
