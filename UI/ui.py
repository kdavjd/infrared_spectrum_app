from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt
from UI.ButtonPanel.button_panel import ButtonPanel
from UI.GraphicalArea.graphical_area import GraphicalArea

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.buttonPanel = ButtonPanel()
        self.graphicalArea = GraphicalArea()

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.buttonPanel)
        splitter.addWidget(self.graphicalArea)
        splitter.setStretchFactor(1, 4)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
