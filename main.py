import package.live2d.v3 as live2d
import sys
from PyQt5.QtGui import QMouseEvent, QCursor
from PyQt5.QtCore import QTimerEvent, Qt, QPoint
from PyQt5.QtWidgets import *
from OpenGL.GL import *

from show_model import ShowModel
from text_window import TextWindow
from show_text import ShowText
live2d.init()

app = QApplication(sys.argv)
show_model = ShowModel()
show_model.show()
text_window = TextWindow()
text_window.show()

show_text = ShowText()
show_text.show()
show_text.updateText("Hello, I'm Open-Source Sama")
sys.exit(app.exec_())
