from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import pyqtSignal, QObject
import pandas as pd
from logger_config import logger


class SpectrumDataFrame(QObject):
    def __init__(self):
        super().__init__()
        self.column_names = ["Длина_волны", "Интенсивность"]
        
    spectrum_loaded = pyqtSignal(pd.DataFrame)
    plot_spectrum = pyqtSignal(pd.DataFrame, list)
    
    def load_spectrum_txt(self):        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(caption="Open Text File", filter="Text Files (*.txt)")
        if file_path:
            try:
                self.df = pd.read_csv(
                    file_path, delim_whitespace=True, header=None, skiprows=1, names=self.column_names)
                self.spectrum_loaded.emit(self.df)
                self.plot_spectrum.emit(self.df, self.column_names)
                logger.debug(f"data head {self.df.head()}")
                return self.df
            except Exception as e:
                logger.warning(f"Ошибка при загрузке файла: {e}")
                return None
        else:
            logger.info("Файл не выбран")
            return None
       