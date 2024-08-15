import package.live2d.v3 as live2d
import sys
from PyQt5.QtGui import QMouseEvent, QCursor
from PyQt5.QtCore import QTimerEvent, Qt, QPoint
from PyQt5.QtWidgets import *
from OpenGL.GL import *

import show_model

live2d.init()

app = QApplication(sys.argv)
win = show_model.Win()
win.show()
#win.showFullScreen()
sys.exit(app.exec_())