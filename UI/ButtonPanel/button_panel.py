from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from .load_button import LoadButton
from .print_button import PrintButton
from .spectrum_table import SpectrumTable

class ButtonPanel(QWidget):
    def __init__(self, spectrum_data_frame):
        super().__init__()        
        
        layout = QVBoxLayout()

        self.load_button = LoadButton(spectrum_data_frame)
        self.print_button = PrintButton()
        self.spectrum_table = SpectrumTable()

        layout.addWidget(self.load_button)
        layout.addWidget(self.print_button)
        layout.addWidget(self.spectrum_table)  
        
        self.setLayout(layout)

        