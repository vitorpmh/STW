from annotation import MainWindow
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = MainWindow(app)
window.show()
sys.exit(app.exec())