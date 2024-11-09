from model import updateProcess, getListProcess, VProcess
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton

def main():
    app = QApplication(sys.argv)

    # Criar a janela principal
    window = QWidget()
    window.setWindowTitle("Tabela de Itens")
    window.setFixedSize(500, 300)

    # Layout principal
    layout = QVBoxLayout()

    # Criar o QTableWidget (tabela)
    table = QTableWidget()
    table.setRowCount(3)  # Número de linhas
    table.setColumnCount(3)  # Número de colunas
    table.setHorizontalHeaderLabels(["Nome", "Valor", "Descrição"])

    # Adicionar itens à tabela (Nome, Valor, Descrição)
    table.setItem(0, 0, QTableWidgetItem("Produto A"))
    table.setItem(0, 1, QTableWidgetItem("R$ 10,00"))
    table.setItem(0, 2, QTableWidgetItem("Descrição do Produto A"))

    table.setItem(1, 0, QTableWidgetItem("Produto B"))
    table.setItem(1, 1, QTableWidgetItem("R$ 20,00"))
    table.setItem(1, 2, QTableWidgetItem("Descrição do Produto B"))

    table.setItem(2, 0, QTableWidgetItem("Produto C"))
    table.setItem(2, 1, QTableWidgetItem("R$ 30,00"))
    table.setItem(2, 2, QTableWidgetItem("Descrição do Produto C"))

    # Função para mostrar o item selecionado
    def show_selected_item():
        selected_item = table.currentItem()
        if selected_item:
            row = table.currentRow()
            col = table.currentColumn()
            print(f"Item selecionado: {table.item(row, 0).text()} - {table.item(row, 1).text()} - {table.item(row, 2).text()}")
        else:
            print("Nenhum item selecionado")

    # Botão para mostrar item selecionado
    button = QPushButton("Mostrar item selecionado")
    button.clicked.connect(show_selected_item)

    # Adicionar widgets ao layout
    layout.addWidget(table)
    layout.addWidget(button)

    # Definir o layout da janela principal
    window.setLayout(layout)

    # Exibir a janela
    window.show()

    # Iniciar o loop da aplicação
    sys.exit(app.exec())

# Executar a função principal
if __name__ == "__main__":
    updateProcess()
    a = getListProcess()
    for b in a:
        b.getInfo()
    main()
