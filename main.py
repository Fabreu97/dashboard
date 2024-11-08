import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QVBoxLayout, QTableWidget
from Button import Button, Geometry

def clickevent() -> None:
    #valor = le.text()
    valor: str = str(combo.currentText())
    label.setText(valor)
    label.adjustSize()

class Button(QPushButton):
    def __init__(self, text: str, window: QWidget = None, geometry: Geometry = None) -> None:
        if(window is not None):
            super().__init__(text, window)
            self.wsize = window.size()
            if(geometry is not None):
                self.setGeometry(geometry.posx - geometry.width//2, geometry.posy - geometry.height//2, geometry.width, geometry.height)
        else:
            super().__init__(text)
        self.ratio: float = window.size().width() / window.size().height()
app = QApplication(sys.argv)
window = QWidget()
window.resize(800,600)
window.setWindowTitle("First Window")
button = Button("My Button", window, Geometry(window.size().width()//2, window.size().height()//2, 150, 100))
button.setStyleSheet('background-color: Blue;color: White')

label = QLabel("Label", window)
label.move(100,300)
label.setStyleSheet('font-size: 30px')
button.clicked.connect(clickevent)

combo = QComboBox(window)
combo.addItem("Selecione uma linguagem de programação") # Primeiro item é o que voce quer q o usuario visualize no menu
combo.addItem("Java")
combo.addItem("Python")
combo.addItem("C")
combo.addItem("C++")
combo.move(10,10)
main_layout = QVBoxLayout()
table = QTableWidget(0, 3)
table.setHorizontalHeaderLabels(["Nome", "Preço", "Quantidade"])

le = QLineEdit("", window)
le.setGeometry(500, 500, 150, 30)

window.show()
app.exec()