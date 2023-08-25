import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from src.gui import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())