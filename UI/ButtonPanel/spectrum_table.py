from PyQt6.QtWidgets import QTableView, QSizePolicy, QAbstractScrollArea
from PyQt6.QtCore import  pyqtSlot
from pandas_model import PandasModel
import pandas as pd
from logger_config import logger

class SpectrumTable(QTableView):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setFixedHeight(300)        

    @pyqtSlot(pd.DataFrame)
    def update_table(self, dataframe):
        logger.debug('Сигнал о новой таблице получен')
        self.spectrum_model = PandasModel(dataframe)
        self.spectrum_model.data_changed_signal.connect(
            self.config.update_config
        )
        self.setModel(self.spectrum_model)