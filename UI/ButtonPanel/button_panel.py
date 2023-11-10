from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget

class ButtonPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.loadButton = QPushButton('Load')
        self.printButton = QPushButton('Print')

        layout.addWidget(self.loadButton)
        layout.addWidget(self.printButton)

        self.setLayout(layout)
