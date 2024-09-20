from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer, Qt

class countdown_app(QWidget):
    def __init__(self, countdown_seconds, configs):
        self.time_remaining = countdown_seconds

        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(200, 50)

        container = QWidget(self)

        # set to left bottom of the screen
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_height = screen_geometry.height()
        self.setGeometry(0, screen_height - self.height(), self.width(), self.height())

        font_color = configs.get('window', 'color')
        self.label = QLabel(f'00:00:00', container)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setStyleSheet(f'color: {font_color};')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont(configs.get('window', 'font'), configs.get('window', 'size')))

        self.shadow_label = QLabel(f'00:00:00', container)
        self.shadow_label.setAttribute(Qt.WA_TranslucentBackground)
        self.shadow_label.setStyleSheet('color: rgba(255, 255, 255, 0.5);')
        self.shadow_label.setAlignment(Qt.AlignCenter)
        self.shadow_label.setFont(QFont(configs.get('window', 'font'), configs.get('window', 'size')))

        self.label.setGeometry(0, 0, 200, 50)
        self.shadow_label.setGeometry(1, 1, 200, 50)

        self.label.raise_()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

    def update_countdown(self):
        self.time_remaining -= 1

        hours, remainder = divmod(self.time_remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.label.setText(f'{hours:02}:{minutes:02}:{seconds:02}')
        self.shadow_label.setText(f'{hours:02}:{minutes:02}:{seconds:02}')

        if self.time_remaining <= 0:
            self.timer.stop()
            self.label.setText('WORK OUT!!!')
            self.shadow_label.setText('WORK OUT!!!')
            QTimer.singleShot(5000, self.close)
