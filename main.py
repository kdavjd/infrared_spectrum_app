import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from UI.ui import UI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from spectrum_data_frame import SpectrumDataFrame
from config import SpectrumConfig
from gaussian_params import GaussianParams
from logger_config import logger

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.spectrum_data_frame = SpectrumDataFrame()     
        self.config = SpectrumConfig()
        self.gaussian_params = GaussianParams()
        self.ui = UI(self.spectrum_data_frame, self.config, self.gaussian_params)        
        self.setCentralWidget(self.ui)
        self.setWindowTitle('Spectrum Analysis Tool')
        self.spectrum_data_frame.spectrum_loaded_signal.connect(
            self.ui.button_panel.spectrum_table.update_table)
        self.ui.graphical_area.toolbar.integral_action_signal.connect(
            self.ui.button_panel.spectrum_table.update_table)
        self.ui.graphical_area.toolbar.gauss_action_signal.connect(
            self.ui.button_panel.spectrum_table.update_table)
        self.ui.graphical_area.gauss_released_signal.connect(
            self.ui.button_panel.spectrum_table.update_table)       
        self.spectrum_data_frame.plot_spectrum_signal.connect(
            self.ui.graphical_area.plot_data)
        self.ui.graphical_area.mouse_released_signal.connect(
            self.spectrum_data_frame.subctract_slice_background)
        self.ui.graphical_area.toolbar.restore_df_plot_signal.connect(
            self.spectrum_data_frame.plot_spectrum)
        self.ui.graphical_area.toolbar.restore_df_plot_signal.connect(
            self.ui.graphical_area.gauss_callbacks.reset_gaussian_params) 
        self.gaussian_params.data_changed_signal.connect(
            self.ui.graphical_area.draw_curves
        )
        
def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
