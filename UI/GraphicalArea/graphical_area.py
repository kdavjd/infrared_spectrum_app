from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import scienceplots
import pandas as pd
import numpy as np
from scipy import signal
from config import SpectrumConfig
from .custom_toolbar import CustomToolbar
from .integral_action_callbacks import IntegralActionCallbacks
from .gauss_action_callbacks import GaussActionCallbacks
from logger_config import logger
plt.style.use(['science', 'no-latex', 'nature', 'grid'])


class GraphicalArea(QWidget):
    
    # Определение сигналов
    mouse_released_signal = pyqtSignal(tuple)
    
    def __init__(self, config, graphical_area=None):
        super().__init__(graphical_area)
        self.config = config      
        # Создание фигуры и осей для графика
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)        
        # Создание пользовательской панели инструментов
        self.toolbar = CustomToolbar(self.canvas, self)
        # настройка поведения кастомных действий панели инструментов
        self.integral_callbacks = IntegralActionCallbacks(self)
        self.gauss_callbacks = GaussActionCallbacks(self)
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
    
    def on_mouse_press(self, event):
        if event.inaxes:
            if event.button == 3 or event.button == 2:
                self.toolbar.deactivate_all_actions()
            if self.toolbar.integral_action.isChecked():
                if event.button == 1:
                    self.integral_callbacks.on_press(event)
            if self.toolbar.gauss_action.isChecked():
                if event.button == 1:
                    self.gauss_callbacks.on_press(event)                            
    
    def on_mouse_move(self, event):
        if self.toolbar.integral_action.isChecked() and self.mouse_pressed and event.xdata and event.inaxes:
            self.integral_callbacks.on_move(event)
        if self.toolbar.gauss_action.isChecked() and self.mouse_pressed and event.xdata and event.inaxes:
            self.gauss_callbacks.on_move(event)
    
    def on_mouse_release(self, event):
        if self.toolbar.integral_action.isChecked() and event.inaxes:
            self.integral_callbacks.on_release(event)
            self.display_integral_value(event)             
        if self.toolbar.gauss_action.isChecked() and event.inaxes:
            self.gauss_callbacks.on_release(event)
    
    def display_integral_value(self, event):
        # Проверяем, что обе координаты x не None
        if self.press_x is not None and event.xdata is not None:
            # Определяем начальную и конечную точки для интегрирования
            start_x = min(self.press_x, event.xdata)
            end_x = max(self.press_x, event.xdata)            
            # Выбираем данные для интегрирования
            mask = (self.x_data >= start_x) & (self.x_data <= end_x)
            x_selected = self.x_data[mask]
            y_selected = self.y_data[mask]
            # Вычисляем интеграл
            integral_value = np.trapz(y_selected, x_selected)
            # Отображаем значение интеграла на графике
            self.ax.text(0.95, 0.05, f'Площадь: {integral_value:.2f}',
                         verticalalignment='bottom', horizontalalignment='right',
                         transform=self.ax.transAxes, fontsize=8, bbox=dict(facecolor='white', alpha=0.5))
            # Перерисовываем холст
            self.canvas.draw()
    
    # Слот для отображения данных на графике
    @pyqtSlot(pd.DataFrame, list)
    def plot_data(self, df, column_names):        
        self.ax.clear()
        self.x_data = df[column_names[0]]
        self.y_data = signal.savgol_filter(
            df[column_names[1]], 
            window_length=self.config.Savitzky_df['window_length'].astype(int).item(),
            polyorder=self.config.Savitzky_df['polyorder'].astype(int).item(), 
            mode=self.config.Savitzky_df['Savitzky_mode'].astype(str).item()) 
        logger.debug(f"Значения Savitzky_df в plot_data: {self.config.Savitzky_df}")       
        # Построение графика по заданным данным
        self.ax.plot(self.x_data, self.y_data)          
        self.canvas.draw()

