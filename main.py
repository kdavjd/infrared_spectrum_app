import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from UI.ui import UI

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UI()
        self.setCentralWidget(self.ui)
        self.setWindowTitle('Spectrum Analysis Tool')

def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
