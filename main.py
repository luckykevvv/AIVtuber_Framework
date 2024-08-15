import package.live2d.v3 as live2d
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

from show_model import ShowModel
from text_window import TextWindow
from show_text import ShowText
from gpt_api import ChatGPT

live2d.init()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show_model = ShowModel()
        self.show_model.show()
        
        self.text_window = TextWindow()
        self.text_window.show()
        
        self.show_text = ShowText()
        self.show_text.show()
        self.show_text.updateText("Hello, I'm Open-Source Sama")

        self.chat = ChatGPT()

        # Set up a timer to check the text_window.show_text attribute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_text_window)
        self.timer.start(1000)  # Check every 1 second

    def check_text_window(self):
        show=self.text_window.get_text()
        if show:
            self.show_text.updateText(self.chat.asking(show))

app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
