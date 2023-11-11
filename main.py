import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from UI.ui import UI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from spectrum_data_frame import SpectrumDataFrame
from data_visualizer import DataVisualizer
from logger_config import logger

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.spectrum_data_frame = SpectrumDataFrame()        
        self.data_visualizer = DataVisualizer()
        self.ui = UI(self.spectrum_data_frame, self.data_visualizer)
        self.setCentralWidget(self.ui)
        self.setWindowTitle('Spectrum Analysis Tool')
        self.spectrum_data_frame.spectrum_loaded.connect(self.ui.button_panel.spectrum_table.update_table)

def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
