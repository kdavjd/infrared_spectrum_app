from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import scienceplots
import pandas as pd
from .custom_toolbar import CustomToolbar 
plt.style.use(['science', 'no-latex', 'nature', 'grid'])
       

class GraphicalArea(QWidget):
    
    # Определение сигналов
    mouse_released_signal = pyqtSignal(tuple)
    
    def __init__(self, parent=None):
        super().__init__(parent)        
        # Создание фигуры и осей для графика
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Создание пользовательской панели инструментов
        self.toolbar = CustomToolbar(self.canvas, self)

        # Инициализация переменных для управления затенением и масштабом
        self.shading_regions = []  # Список для хранения затемненных областей
        self.original_xlim = None  # Исходный масштаб оси X
        self.press_x = None        # Координата X при нажатии мыши
        self.press_y = None        # Координата Y при нажатии мыши
        self.mouse_pressed = False # Флаг состояния нажатия мыши

        # Подключение обработчиков событий мыши
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)        

        # Размещение элементов в макете
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    # Обработчик события нажатия кнопки мыши
    def on_mouse_press(self, event):
        if self.toolbar.integral_action and event.inaxes:
            self.mouse_pressed = True
            self.press_x = event.xdata
            self.original_xlim = self.ax.get_xlim()  # Сохранение текущего масштаба оси X
            self.ax.set_facecolor('white')
            self.canvas.draw()

    # Обработчик перемещения мыши с зажатой кнопкой
    def on_mouse_move(self, event):
        if self.toolbar.integral_action and self.mouse_pressed and event.xdata and event.inaxes:
            for region in self.shading_regions:
                region.remove()
            self.shading_regions.clear()

            self.ax.set_xlim(self.original_xlim)  # Фиксация масштаба оси X

            # Создание затемненных областей в зависимости от положения мыши
            if event.xdata < self.press_x:
                region1 = self.ax.axvspan(self.ax.get_xlim()[0], event.xdata, color='gray', alpha=0.5)
                region2 = self.ax.axvspan(self.press_x, self.ax.get_xlim()[1], color='gray', alpha=0.5)
            else:
                region1 = self.ax.axvspan(self.ax.get_xlim()[0], self.press_x, color='gray', alpha=0.5)
                region2 = self.ax.axvspan(event.xdata, self.ax.get_xlim()[1], color='gray', alpha=0.5)

            self.shading_regions.extend([region1, region2])
            self.canvas.draw()

    # Обработчик события отпускания кнопки мыши
    def on_mouse_release(self, event):
        if self.toolbar.integral_action:
            self.mouse_pressed = False
            for region in self.shading_regions:
                region.remove()
            self.shading_regions.clear()
            self.ax.set_xlim(self.original_xlim)
            self.canvas.draw()
            # Испускание сигнала с координатами
            if self.press_x is not None and event.xdata is not None:
                self.mouse_released_signal.emit((self.press_x, event.xdata))
    
    # Слот для отображения данных на графике
    @pyqtSlot(pd.DataFrame, list)
    def plot_data(self, df, column_names):        
        self.ax.clear()
        # Построение графика по заданным данным
        self.ax.plot(df[column_names[0]], df[column_names[1]],)          
        self.canvas.draw()
