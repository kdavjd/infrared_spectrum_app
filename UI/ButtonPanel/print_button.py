from PyQt6.QtWidgets import QPushButton

class PrintButton(QPushButton):
    def __init__(self, data_visualizer):
        super().__init__('Print')
        self.data_visualizer = data_visualizer
        self.clicked.connect(self.on_click)

    def on_click(self):
        self.data_visualizer.plot_data()
