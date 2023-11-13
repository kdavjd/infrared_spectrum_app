import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from UI.ui import UI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from spectrum_data_frame import SpectrumDataFrame

from logger_config import logger

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.spectrum_data_frame = SpectrumDataFrame()      
        
        self.ui = UI(self.spectrum_data_frame)
        self.setCentralWidget(self.ui)
        self.setWindowTitle('Spectrum Analysis Tool')
        self.spectrum_data_frame.spectrum_loaded.connect(self.ui.button_panel.spectrum_table.update_table)
        self.spectrum_data_frame.plot_spectrum.connect(self.ui.graphical_area.plot_data)
        self.ui.graphical_area.mouse_released.connect(self.spectrum_data_frame.modify_dataframe)

def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
