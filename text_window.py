from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QScreen
from PyQt5.QtCore import Qt, QPoint, QEvent

class TextWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Text Input Window")
        self.resize(1500, 200)  # Adjust the window size

        # Create QVBoxLayout
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        # Create horizontal layout
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)
        
        # Set the spacing and margins of the horizontal layout to 0
        h_layout.setSpacing(0)
        h_layout.setContentsMargins(0, 0, 0, 0)

        # Create QLineEdit
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter text here...")
        
        # Set font
        font = QFont()
        font.setPointSize(20)  # Set font size to 20
        self.text_input.setFont(font)
        
        self.text_input.setMinimumHeight(100)  # Set minimum height
        
        # Set style
        self.text_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(0, 0, 0, 150); /* Black-gray semi-transparent background */
                color: white; /* White input text */
                border: none; /* Remove border */
                padding: 10px; /* Add padding */
            }
        """)
        
        # Create drag button
        self.drag_button = QPushButton("||", self)
        self.drag_button.setFixedSize(60, 100)  # Set button size, same height as the text box
        
        # Set button style
        self.drag_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 150); /* Black-gray semi-transparent background */
                color: white; /* White button text */
                border: none; /* Remove border */
                padding: 10px; /* Add padding */
            }
            QPushButton:hover {
                background-color: rgba(50, 50, 50, 150); /* Color when hovering */
            }
        """)

        # Add the button and text box to the horizontal layout
        h_layout.addWidget(self.text_input)
        h_layout.addWidget(self.drag_button)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        
        self.dragging = False
        self.offset = QPoint()

        # Connect the returnPressed signal to the slot function
        self.text_input.returnPressed.connect(self.save_text)
        self.saved_text = ""  # Variable to store the text
        
        # Set the drag button's mouse event filter
        self.drag_button.installEventFilter(self)
        
        self.center_in_bottom()
        
    def save_text(self):
        """Save the text box content to a variable and clear the text box"""
        self.saved_text = self.text_input.text()
        print(f"Saved text: {self.saved_text}")  # Print the saved text for verification
        self.text_input.clear()  # Clear the text box
        
    def get_text(self):
        ret=self.saved_text
        self.saved_text=None
        return ret
        
    def eventFilter(self, obj, event):
        """Event filter to handle drag button events"""
        if obj == self.drag_button:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.startDragging(event.globalPos())
                return True
            elif event.type() == QEvent.MouseMove and self.dragging:
                self.dragWindow(event.globalPos())
                return True
            elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
                self.stopDragging()
                return True
        return super().eventFilter(obj, event)
    
    def center_in_bottom(self):
        screen_geometry = QScreen.availableGeometry(QApplication.primaryScreen())
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # calculate the new pozition
        x = (screen_width - self.width()) // 2
        y = screen_height - (screen_height // 20) - (self.height() // 2)
        
        self.move(x, y)

    
    def startDragging(self, global_pos) -> None:
        """Start dragging"""
        self.dragging = True
        self.offset = global_pos - self.pos()

    def dragWindow(self, global_pos) -> None:
        """Drag the window"""
        if self.dragging:
            new_position = global_pos - self.offset
            self.move(new_position)

    def stopDragging(self) -> None:
        """Stop dragging"""
        self.dragging = False
