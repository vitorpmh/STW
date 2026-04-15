from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QWheelEvent
from PySide6.QtCore import Qt

class ZoomableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.pixmap_original = None
        self.current_scale = 1.0
        self.zoom_factor = 0.05  # Define the zoom increment factor

    def setPixmap(self, pixmap):
        self.pixmap_original = pixmap
        super().setPixmap(pixmap)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            super().wheelEvent(event)

    def zoom_in(self):
        self.current_scale += self.zoom_factor
        self.scale()

    def zoom_out(self):
        self.current_scale -= self.zoom_factor
        self.scale()

    def scale(self):
        if self.pixmap_original:
            size = self.pixmap_original.size()
            new_size = size * self.current_scale
            #if new_size.toTuple()[0]<= size.toTuple()[0]:
            scaled_pixmap = self.pixmap_original.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            #else:
            scaled_pixmap = self.pixmap_original.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            super().setPixmap(scaled_pixmap)
