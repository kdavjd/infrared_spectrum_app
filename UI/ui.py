from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt, QSize
from UI.GraphicalArea.graphical_area import GraphicalArea
from UI.ButtonPanel.button_panel import ButtonPanel

class UI(QWidget):
    def __init__(self, spectrum_data_frame, data_visualizer):
        super().__init__()
        # Установка минимального размера окна
        self.setMinimumSize(QSize(920, 780)) 
        
        self.graphical_area = GraphicalArea()
        self.button_panel = ButtonPanel(data_visualizer, spectrum_data_frame)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.button_panel)
        splitter.addWidget(self.graphical_area)
        splitter.setStretchFactor(1, 4)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
