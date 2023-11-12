from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import  pyqtSlot
from PyQt6.QtGui import QAction, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science', 'no-latex', 'nature', 'grid'])
import pandas as pd


class CustomToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)
        
        integral_icon_path = 'icons\integral_icon.png' 

        self.integral_action = QAction(QIcon(integral_icon_path), '', self)
        self.integral_action.setCheckable(True)
        self.integral_action.triggered.connect(self.toggle_integral_mode)
        self.addAction(self.integral_action)
        self.integral_action = False

    def toggle_integral_mode(self):
        self.integral_action = not self.integral_action
        if self.integral_action:
            self.canvas.figure.gca().set_facecolor('white')  # Восстановить цвет при выходе из режима
            self.canvas.draw()


class GraphicalArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = CustomToolbar(self.canvas, self)
        
        self.shading_regions = []  # Для хранения затемнённых областей
        self.original_xlim = None  # Для сохранения исходного масштаба оси X
        self.press_x = None
        self.press_y = None
        self.mouse_pressed = False
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)        

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def on_mouse_press(self, event):
        if self.toolbar.integral_action and event.inaxes:
            self.mouse_pressed = True
            self.press_x = event.xdata
            self.original_xlim = self.ax.get_xlim()  # Сохранить текущий масштаб оси X
            self.ax.set_facecolor('white')
            self.canvas.draw()

    def on_mouse_move(self, event):
        if self.toolbar.integral_action and self.mouse_pressed and event.xdata and event.inaxes:
            for region in self.shading_regions:
                region.remove()
            self.shading_regions.clear()

            self.ax.set_xlim(self.original_xlim)  # Фиксировать масштаб оси X

            if event.xdata < self.press_x:
                region1 = self.ax.axvspan(self.ax.get_xlim()[0], event.xdata, color='gray', alpha=0.5)
                region2 = self.ax.axvspan(self.press_x, self.ax.get_xlim()[1], color='gray', alpha=0.5)
            else:
                region1 = self.ax.axvspan(self.ax.get_xlim()[0], self.press_x, color='gray', alpha=0.5)
                region2 = self.ax.axvspan(event.xdata, self.ax.get_xlim()[1], color='gray', alpha=0.5)

            self.shading_regions.extend([region1, region2])
            self.canvas.draw()

    def on_mouse_release(self, event):
        if self.toolbar.integral_action:
            self.mouse_pressed = False
            for region in self.shading_regions:
                region.remove()
            self.shading_regions.clear()
            self.ax.set_xlim(self.original_xlim)
            self.canvas.draw()
    
    @pyqtSlot(pd.DataFrame, list)
    def plot_data(self, df, column_names):
        self.ax.clear()
        self.ax.plot(df[column_names[0]], df[column_names[1]],)          
        self.canvas.draw()
