import package.live2d.v3 as live2d
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot
from gtts import gTTS
from pydub import AudioSegment
import pygame
from show_model import ShowModel
from text_window import TextWindow
from show_text import ShowText
from gpt_api import ChatGPT

live2d.init()

class ChatGPTThread(QThread):
    response_ready = pyqtSignal(str)

    def __init__(self, input_text):
        super().__init__()
        self.input_text = input_text
        self.chat = ChatGPT()

    def run(self):
        response = self.chat.asking(self.input_text)
        self.response_ready.emit(response)

class AudioProcessingThread(QThread):
    audio_ready = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        tts = gTTS(text=self.text, lang='en', slow=False)
        tts.save('./live_2d_model/hiyori_free_en/runtime/sounds/test.mp3')
        
        sound = AudioSegment.from_mp3("./live_2d_model/hiyori_free_en/runtime/sounds/test.mp3")
        sound.export("./live_2d_model/hiyori_free_en/runtime/sounds/test.wav", format="wav")
        
        self.audio_ready.emit("./live_2d_model/hiyori_free_en/runtime/sounds/test.wav")

class ShowModelThread(QThread):
    modelUpdated = pyqtSignal()

    def __init__(self, show_model):
        super().__init__()
        self.show_model = show_model
        self.model = self.show_model.model

    def run(self):
        while True:
            self.msleep(10000)
            self.modelUpdated.emit()

    @pyqtSlot()
    def updateModel(self):
        if self.model.IsMotionFinished():
            self.model.SetLipSyncEnable(True)
            self.model.Update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.show_model = ShowModel()
        self.show_model.show()
        
        self.show_model_thread = ShowModelThread(self.show_model)
        self.show_model_thread.modelUpdated.connect(self.updateShowModel)
        self.show_model_thread.start()
        
        self.text_window = TextWindow()
        self.text_window.show()
        
        self.show_text = ShowText()
        self.show_text.show()
        self.show_text.updateText("Hello, I'm Open-Source Sama")

        # Set up a timer to check the text_window.show_text attribute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_text_window)
        self.timer.start(1000)

    def check_text_window(self):
        show = self.text_window.get_text()
        if show:
            self.chat_thread = ChatGPTThread(show)
            self.chat_thread.response_ready.connect(self.handleResponse)
            self.chat_thread.start()

    @pyqtSlot(str)
    def handleResponse(self, response):
        self.show_text.updateText(response)
        
        # Start audio processing in a separate thread
        self.audio_thread = AudioProcessingThread(response)
        self.audio_thread.audio_ready.connect(self.playAudio)
        self.audio_thread.start()

    @pyqtSlot(str)
    def playAudio(self, wav_file_path):
        if self.show_model.model.IsMotionFinished():
            pygame.init()
            pygame.mixer.init()
            self.show_model.model.StartMotion("Idle", 3, live2d.MotionPriority.FORCE.value)
            pygame.mixer.Sound(wav_file_path).play()

    @pyqtSlot()
    def updateShowModel(self):
        self.show_model_thread.updateModel()
        self.show_model.update()

app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
