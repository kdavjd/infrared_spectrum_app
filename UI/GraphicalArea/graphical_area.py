from PyQt6.QtWidgets import QWidget
from data_visualizer import DataVisualizer 

class GraphicalArea(QWidget):
    def __init__(self):
        super().__init__()
        self.visualizer = DataVisualizer(self)

    def plot_data(self, data):
        self.visualizer.plot_data(data)
