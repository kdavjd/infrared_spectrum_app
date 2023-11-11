from PyQt6.QtWidgets import QPushButton

class LoadButton(QPushButton):
    def __init__(self, spectrum_data_frame):
        super().__init__('Load')
        self.spectrum_data_frame = spectrum_data_frame
        self.clicked.connect(self.on_click)

    def on_click(self):
        self.spectrum_data_frame.load_spectrum_txt()
