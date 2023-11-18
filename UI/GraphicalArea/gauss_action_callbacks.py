import numpy as np
import pandas as pd

class GaussActionCallbacks:
    def __init__(self, graphical_area):
        self.graphical_area = graphical_area
        self.gaussian_params = pd.DataFrame(columns=['Height', 'Position', 'Width'])

    def on_press(self, event):
        self.graphical_area.mouse_pressed = True
        self.press_x = event.xdata        
        self.gaussian_drawn = False

    def on_move(self, event):
        if event.inaxes and self.graphical_area.mouse_pressed:
            w = 2 * abs(self.press_x - event.xdata)
            x_data = self.graphical_area.ax.lines[0].get_xdata()
            x = np.linspace(min(x_data), max(x_data), 1000)
            y = self.gaussian(x, event.ydata, self.press_x, w)
            if self.gaussian_drawn:
                self.graphical_area.ax.lines[-1].set_xdata(x)
                self.graphical_area.ax.lines[-1].set_ydata(y)
            else:
                self.graphical_area.ax.plot(x, y, 'r--')
                self.gaussian_drawn = True
            self.graphical_area.canvas.draw()
        
    def on_release(self, event):
        self.graphical_area.mouse_pressed = False
        if self.gaussian_drawn:
            new_row = pd.DataFrame({'Height': [event.ydata],
                                    'Position': [self.press_x],
                                    'Width': [2 * abs(self.press_x - event.xdata)]})
            self.gaussian_params = pd.concat([self.gaussian_params, new_row], ignore_index=True)
            self.gaussian_drawn = False
    
    @staticmethod
    def gaussian(x: np.ndarray, h: float, z: float, w: float) -> np.ndarray:        
        return h * np.exp(-((x - z) ** 2) / (2 * w ** 2))