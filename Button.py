from PyQt6.QtWidgets import QWidget, QPushButton

class Geometry:
    def __init__(self, posx: int, posy: int, width: int, height: int):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height

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