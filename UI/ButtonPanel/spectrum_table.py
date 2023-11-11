from PyQt6.QtWidgets import QTableWidget, QTableView, QVBoxLayout, QWidget
from PyQt6.QtCore import  pyqtSlot
from pandas_model import PandasModel
import pandas as pd

class SpectrumTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableView()
        self.table_layout = QVBoxLayout() # Под вопросом
        self.table_layout.addWidget(self.table)
        table_widget = QWidget()
        table_widget.setLayout(self.table_layout)        
    
    @pyqtSlot(pd.DataFrame)
    def update_table(self, dataframe):
        print('Сигнал получен')
        self.spectrum_model = PandasModel(dataframe)
        self.table.setModel(self.spectrum_model)