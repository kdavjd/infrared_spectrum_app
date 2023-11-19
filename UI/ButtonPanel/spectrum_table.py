from PyQt6.QtWidgets import QTableView, QSizePolicy, QAbstractScrollArea
from PyQt6.QtCore import  pyqtSlot
from pandas_model import PandasModel
import pandas as pd
from logger_config import logger

class SpectrumTable(QTableView):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(300)        

    @pyqtSlot(pd.DataFrame)
    def update_table(self, dataframe):
        logger.debug('Сигнал о новой таблице получен')
        self.spectrum_model = PandasModel(dataframe)
        self.setModel(self.spectrum_model)