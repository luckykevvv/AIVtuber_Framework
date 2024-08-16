import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ShowText(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.8)
        
        # Create a QTextEdit to display text
        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet('color: white; font-size: 60px; background: transparent; border: none;')  # Increase font size, set background transparent and remove border
        self.text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.text_edit.setAlignment(Qt.AlignCenter)
        self.text_edit.setWordWrapMode(QTextOption.WrapAnywhere)  # Set word wrap mode
        self.text_edit.setMinimumSize(2000, 400)  # Increase minimum width to 1200 pixels
        
        # Hide scrollbars
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Create a layout and add the text edit
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.setContentsMargins(10, 10, 10, 10)  # Margins to keep text away from window edges
        self.setLayout(layout)

        # Set the initial size of the window
        self.resize(2000, 400)  # Adjust initial size to fit wider text box

        # Use a QTimer to ensure the window is fully shown before positioning
        QTimer.singleShot(0, self.center_in_bottom)
        
        # Animation setup
        self.animation = QPropertyAnimation(self.text_edit.verticalScrollBar(), b"value")
        self.animation.setDuration(5000)  # Duration of animation in milliseconds
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)  # Smooth easing curve

    def updateText(self, text):
        self.text_edit.setPlainText(text)
        self.adjust_size()

        # Start scrolling to the bottom if the text exceeds the visible area
        if self.text_edit.verticalScrollBar().maximum() > self.text_edit.verticalScrollBar().value():
            self.animate_scroll_to_bottom()

    def adjust_size(self):
        # Resize the window to fit the new text size
        self.text_edit.adjustSize()
        new_size = self.text_edit.size()
        self.resize(max(new_size.width() + 20, 1200), new_size.height() + 20)  # Ensure a minimum width of 1200
        self.text_edit.setFixedSize(self.size())  # Ensure text edit size matches window size
        self.update()  # Trigger a repaint
        self.center_in_bottom()

    def animate_scroll_to_bottom(self):
        scroll_bar = self.text_edit.verticalScrollBar()
        start_value = scroll_bar.value()
        end_value = scroll_bar.maximum()

        self.animation.setStartValue(start_value)
        self.animation.setEndValue(end_value)
        self.animation.start()

    def paintEvent(self, event):
        # Paint the background with a semi-transparent color
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))  # RGBA color for semi-transparency
        painter.drawRect(self.rect())
        
    def center_in_bottom(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate the new position
        x = (screen_width - self.width()) // 2
        y = screen_height - (screen_height // 4) - (self.height() // 2)  # Adjust y for bottom margin (50 pixels from the bottom)

        self.move(QPoint(x, y))

