from PyQt6.QtWidgets import QPushButton

class PrintButton(QPushButton):
    def __init__(self):
        super().__init__('Построить график')
        self.clicked.connect(self.on_click)  
              
    def on_click(self):
        pass

    
