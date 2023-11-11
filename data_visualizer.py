import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DataVisualizer(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.setParent(parent)

    def plot_data(self, data):
        # Предполагая, что data - это список числовых значений
        self.ax.clear()
        self.ax.plot(data)
        self.draw()
