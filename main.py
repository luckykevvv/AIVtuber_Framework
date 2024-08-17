import package.live2d.v3 as live2d
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
#from ffmpeg import audio
from show_model import ShowModel
from text_window import TextWindow
from show_text import ShowText
from gpt_api import ChatGPT
from gtts import gTTS
from pydub import AudioSegment
#import pyttsx3
#from audiostretchy.stretch import stretch_audio
import pygame

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
        #self.engine = pyttsx3.init()

        # Set up a timer to check the text_window.show_text attribute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_text_window)
        self.timer.start(1000)  # Check every 1 second

    def check_text_window(self):
        show=self.text_window.get_text()
        if show:
            result=self.chat.asking(show)
            tts = gTTS(text=result, lang='en',slow=False)
            tts.save('./live_2d_model/hiyori_free_en/runtime/sounds/test.mp3')
            
            sound = AudioSegment.from_mp3("live_2d_model/hiyori_free_en/runtime/sounds/test.mp3")
            sound.export("live_2d_model/hiyori_free_en/runtime/sounds/test.wav", format="wav")

            self.show_text.updateText(result)
            
            if self.show_model.model.IsMotionFinished():
                self.show_model.model.SetLipSyncEnable(True)
                self.show_model.model.Update()
                pygame.init()
                pygame.mixer.init()
                self.show_model.model.StartMotion("Idle", 3, live2d.MotionPriority.FORCE.value)
                pygame.mixer.Sound('live_2d_model/hiyori_free_en/runtime/sounds/test.wav').play()
                self.show_model.update() 

app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
