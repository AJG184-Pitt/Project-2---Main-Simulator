from PyQt6.QtGui import QPixmap, QKeyEvent
from PyQt6.QtWidgets import (QApplication, QMainWindow, QComboBox,
                            QLineEdit, QLabel, QGridLayout, QWidget)
from PyQt6.QtCore import Qt, pyqtSignal, QEvent, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size constraints
        self.setWindowTitle("PyQt6 Application for On-Device UI")
        self.setFixedSize(1920, 1080)

        # Create central widget and layout
        central_widget = QWidget()
        background_image = "Assets/star_background"
        central_widget.setStyleSheet(f"""
            QWidget {{
                background-image: url({background_image});            
                background-repeat: no-repeat;
                background-position: center;
            }}
        """)
        self.setCentralWidget(central_widget)
        grid = QGridLayout(central_widget)

        self.combo_box = CustomComboBox()
        options = ['Bus', 'Bundle', 'Transformer']
        self.combo_box.addItems(options)
        self.combo_box.setFixedWidth(400)
        self.combo_box.setFixedHeight(100)
