class IntegralActionCallbacks:
    def __init__(self, graphical_area):
        self.graphical_area = graphical_area
        
    def on_press(self, event):
        self.graphical_area.mouse_pressed = True
        self.graphical_area.press_x = event.xdata
        self.graphical_area.original_xlim = self.graphical_area.ax.get_xlim()
        self.graphical_area.ax.set_facecolor('white')
        self.graphical_area.canvas.draw()

    def on_move(self, event):
        for region in self.graphical_area.shading_regions:
                region.remove()
        self.graphical_area.shading_regions.clear()
        self.graphical_area.ax.set_xlim(self.graphical_area.original_xlim)
        # Создание затемненных областей в зависимости от положения мыши
        if event.xdata < self.graphical_area.press_x:
            region1 = self.graphical_area.ax.axvspan(self.graphical_area.ax.get_xlim()[0], event.xdata, color='gray', alpha=0.5)
            region2 = self.graphical_area.ax.axvspan(self.graphical_area.press_x, self.graphical_area.ax.get_xlim()[1], color='gray', alpha=0.5)
        else:
            region1 = self.graphical_area.ax.axvspan(self.graphical_area.ax.get_xlim()[0], self.graphical_area.press_x, color='gray', alpha=0.5)
            region2 = self.graphical_area.ax.axvspan(event.xdata, self.graphical_area.ax.get_xlim()[1], color='gray', alpha=0.5)
        self.graphical_area.shading_regions.extend([region1, region2])
        self.graphical_area.canvas.draw()
        

    def on_release(self, event):
        self.graphical_area.mouse_pressed = False
        for region in self.graphical_area.shading_regions:
            region.remove()
        self.graphical_area.shading_regions.clear()
        self.graphical_area.ax.set_xlim(self.graphical_area.original_xlim)
        self.graphical_area.canvas.draw()
        # Испускание сигнала с координатами
        if self.graphical_area.press_x is not None and event.xdata is not None:
            self.graphical_area.mouse_released_signal.emit((self.graphical_area.press_x, event.xdata))