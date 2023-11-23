from PyQt6.QtWidgets import QTableView, QSizePolicy, QAbstractScrollArea
from PyQt6.QtCore import  pyqtSlot
from pandas_model import PandasModel
import pandas as pd
from logger_config import logger

class SpectrumTable(QTableView):
    def __init__(self, config, gaussian_params):
        super().__init__()
        self.config = config
        self.gaussian_params = gaussian_params
        self.setFixedHeight(300)        

    @pyqtSlot(pd.DataFrame)
    def update_table(self, dataframe):
        logger.debug('Сигнал о новой таблице получен')
        self.spectrum_model = PandasModel(dataframe)
        if 'window_length' in dataframe.columns:
            self.spectrum_model.data_changed_signal.connect(
                self.config.update_config
            )
        elif 'Height' in dataframe.columns:
            self.spectrum_model.data_changed_signal.connect(
                self.gaussian_params.update_params
            )
        self.setModel(self.spectrum_model)