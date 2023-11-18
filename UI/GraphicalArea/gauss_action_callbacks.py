import numpy as np

class GaussActionCallbacks:
    def __init__(self, graphical_area):
        self.graphical_area = graphical_area

    def on_press(self, event):
        self.press_x = event.xdata
        self.press_y = event.ydata

    def on_move(self, event):
        pass
        

    def on_release(self, event):
        pass
    
    def gaussian(x: np.ndarray, h: float, z: float, w: float) -> np.ndarray:        
        return h * np.exp(-((x - z) ** 2) / (2 * w ** 2))