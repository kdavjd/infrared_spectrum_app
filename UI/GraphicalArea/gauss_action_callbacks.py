import numpy as np
import pandas as pd
from PyQt6.QtCore import pyqtSlot
from logger_config import logger

class GaussActionCallbacks:
    def __init__(self, graphical_area):
        self.graphical_area = graphical_area
        self.gaussian_params = pd.DataFrame(columns=['Height', 'Position', 'Width'])

    def reset_gaussian_params(self):
        self.gaussian_params = pd.DataFrame(columns=['Height', 'Position', 'Width'])
        logger.debug(f"Данные gaussian_params сброшены: {self.gaussian_params}")
    
    def on_press(self, event):
        self.graphical_area.mouse_pressed = True
        self.press_x = event.xdata        
        self.gaussian_drawn = False

    def on_move(self, event):
        if event.inaxes and self.graphical_area.mouse_pressed:
            w = 2 * abs(self.press_x - event.xdata)
            self.x_data = self.graphical_area.ax.lines[0].get_xdata()
            x = np.linspace(min(self.x_data), max(self.x_data), 1000)
            y = self.gaussian(x, event.ydata, self.press_x, w)
            if self.gaussian_drawn:
                self.graphical_area.ax.lines[-1].set_xdata(x)
                self.graphical_area.ax.lines[-1].set_ydata(y)
            else:
                self.graphical_area.ax.plot(x, y)
                self.gaussian_drawn = True
            self.graphical_area.canvas.draw()
        
    def on_release(self, event):
        self.graphical_area.mouse_pressed = False
        if self.gaussian_drawn:
            new_row = pd.DataFrame({'Height': [event.ydata],
                                    'Position': [self.press_x],
                                    'Width': [2 * abs(self.press_x - event.xdata)]})
            self.gaussian_params = pd.concat([self.gaussian_params, new_row], ignore_index=True)
            logger.debug(
                f"Событие отпуска мыши: высота={event.ydata}, позиция={self.press_x}, ширина={2 * abs(self.press_x - event.xdata)}")
            # Перерисовываем все кривые на осях
            self.graphical_area.ax.clear()
            self.graphical_area.ax.plot(self.graphical_area.x_data, self.graphical_area.y_data)
            self.gaussian_params.apply(
                lambda row: self.graphical_area.ax.plot(
                    self.x_data, self.gaussian(self.x_data, row['Height'], row['Position'], row['Width'])
                    ), axis=1)          
            self.graphical_area.ax.plot(self.x_data, self.add_cumulitive_gauss_func())
            self.graphical_area.canvas.draw()
            self.gaussian_drawn = False            
    
    def add_cumulitive_gauss_func(self):
        logger.debug(f"Данные gaussian_params в функции кумулятивной линии: {self.gaussian_params}")        
        return self.gaussian_params.apply(lambda x: self.gaussian(self.x_data, *x), axis=1).sum()
    
    @staticmethod
    def gaussian(x: np.ndarray, h: float, z: float, w: float) -> np.ndarray:             
        return h * np.exp(-((x - z) ** 2) / (2 * w ** 2))
    
    
    