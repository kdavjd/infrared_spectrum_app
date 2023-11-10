from PyQt6.QtWidgets import QWidget

class GraphicalArea(QWidget):
    def __init__(self):
        super().__init__()
        # Инициализация графической области
        self.setStyleSheet("background-color: lightblue;")
