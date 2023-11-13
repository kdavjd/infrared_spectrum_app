from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
import pandas as pd
from logger_config import logger


class SpectrumDataFrame(QObject):
    def __init__(self):
        super().__init__()
        self.column_names = ["Длина_волны", "Интенсивность"]
        
    spectrum_loaded_signal = pyqtSignal(pd.DataFrame)
    plot_spectrum_signal = pyqtSignal(pd.DataFrame, list)
    
    @pyqtSlot()
    def plot_spectrum(self):
        self.plot_spectrum_signal.emit(self.df, self.column_names)
        
    def load_spectrum_txt(self):        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(caption="Open Text File", filter="Text Files (*.txt)")
        if file_path:
            try:
                self.df = pd.read_csv(
                    file_path, delim_whitespace=True, header=None, skiprows=1, names=self.column_names)
                self.spectrum_loaded_signal.emit(self.df)
                self.plot_spectrum()
                logger.debug(f"data head {self.df.head()}")
                return self.df
            except Exception as e:
                logger.warning(f"Ошибка при загрузке файла: {e}")
                return None
        else:
            logger.info("Файл не выбран")
            return None
    
    @pyqtSlot(tuple)
    def modify_dataframe(self, slice_borders: tuple):
        logger.debug(f"Получены новые точки диапазона интегрирования: {slice_borders}")
        lower_bound, upper_bound = sorted(slice_borders)
        
        # Фильтрация DataFrame
        filtered_df = self.df[(self.df["Длина_волны"] >= lower_bound) & (self.df["Длина_волны"] <= upper_bound)].copy()
        
        # Вычисление уравнения прямой
        start_point = filtered_df.iloc[0]
        end_point = filtered_df.iloc[-1]
        m = (end_point["Интенсивность"] - start_point["Интенсивность"]) / (end_point["Длина_волны"] - start_point["Длина_волны"])
        c = start_point["Интенсивность"] - m * start_point["Длина_волны"]
        
        # Нахождение максимального значения для горизонтальной линии
        max_value = filtered_df["Интенсивность"].max()
        
        # Корректировка значений
        filtered_df["Интенсивность"] = filtered_df.apply(
            lambda row: row["Интенсивность"] - (m * row["Длина_волны"] + c) + max_value, axis=1)
        
        self.plot_spectrum_signal.emit(filtered_df, self.column_names)
        
       