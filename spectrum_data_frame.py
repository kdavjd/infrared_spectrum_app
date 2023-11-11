from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import pyqtSignal, QObject
import pandas as pd

class SpectrumDataFrame(QObject):
    def __init__(self):
        super().__init__()
        
    spectrum_loaded = pyqtSignal(pd.DataFrame)
    
    def load_spectrum_txt(self):        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(caption="Open Text File", filter="Text Files (*.txt)")
        if file_path:
            try:
                dataframe = pd.read_csv(file_path, sep='\t')  # Assuming tab-separated values
                return dataframe
            except Exception as e:
                print(f"Error loading file: {e}")
                return None
        else:
            print("No file selected")
            return None