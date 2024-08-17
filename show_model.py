import package.live2d.v3 as live2d
from PyQt5.QtGui import QMouseEvent, QCursor
from PyQt5.QtCore import QTimerEvent, Qt, QPoint
from PyQt5.QtWidgets import *
import pygame

class ShowModel(QOpenGLWidget):
    model: live2d.LAppModel
    
    def __init__(self) -> None:
        super().__init__()
        self.a = 0
        self.model = None 
        self.resize(500, 1000)
        #frame less and transparent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.dragging = False
        self.offset = QPoint()
        
        self.createContextMenu()
        
        screen_rect = QApplication.primaryScreen().geometry()
        window_rect = self.geometry()
        new_x = screen_rect.width() - window_rect.width()
        new_y = screen_rect.height() - window_rect.height()
        self.move(new_x, new_y)
        
    def createContextMenu(self) -> None:
        """Create the context menu with the necessary actions."""
        self.context_menu = QMenu(self)
        close_action = self.context_menu.addAction("Close")
        close_action.triggered.connect(self.endWindow)
    
    def endWindow(self):
        self.killTimer(self.timer_id)
        live2d.dispose()
        QApplication.quit()

    
    def showContextMenu(self, position: QPoint) -> None:
        """Show the context menu at the given position."""
        self.context_menu.exec_(position)
    
    def initializeGL(self):
        self.makeCurrent()
        
        # initialize Glew
        live2d.glewInit()    
        # set the OPENGL
        live2d.setGLProperties()

        #initialize the model
        self.model = live2d.LAppModel()
        self.model.LoadModelJson("./live_2d_model/hiyori_free_en/runtime/hiyori_free_t08.model3.json")
        
        self.model.SetLipSyncN(10.0)
        self.update()
        
        self.timer_id =self.startTimer(int(1000 / 60))

    def resizeGL(self, w, h): 
        self.model.Resize(w, h)

    def paintGL(self) -> None:
        live2d.clearBuffer()
        self.model.CalcParameters()
        self.model.Update()
        
    def timerEvent(self,event):
        if self.a == 0:
           '''self.model.SetLipSyncEnable(True)
            self.model.Update()
            pygame.init()
            pygame.mixer.init()
            self.model.StartMotion("Idle", 3, live2d.MotionPriority.FORCE.value)
            pygame.mixer.Sound('live_2d_model/hiyori_free_en/runtime/sounds/test.wav').play()
            self.a += 1'''
        self.update()
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.model.Touch(event.pos().x(), event.pos().y())
        
        if event.button() == Qt.LeftButton:
            #recording the position
            self.dragging = True
            self.offset = event.pos()
            
        elif event.button() == Qt.RightButton:
            # Show context menu on right-click
            self.showContextMenu(QCursor.pos()) 

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.model.Drag(event.pos().x(), event.pos().y())
        
        if self.dragging:
            #start moving
            new_position = self.pos() + (event.globalPos() - self.offset - self.pos())
            self.move(new_position)
            self.offset = event.globalPos() - self.pos()
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
            
if __name__ == "__main__":
    import sys
    live2d.init()
    app = QApplication(sys.argv)
    show_model = ShowModel()
    show_model.show()
    sys.exit(app.exec_())