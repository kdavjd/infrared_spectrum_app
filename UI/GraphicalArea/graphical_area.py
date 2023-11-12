from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import  pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pandas as pd

class GraphicalArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    @pyqtSlot(pd.DataFrame, list)
    def plot_data(self, df, column_names):
        self.ax.clear()
        self.ax.plot(df[column_names[0]], df[column_names[1]],)
        self.ax.grid()
        self.canvas.draw()
