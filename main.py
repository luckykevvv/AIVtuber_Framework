import sys
import threading
import numpy as np
import pygame
import sounddevice as sd
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, pyqtSignal, QThread
from show_model import ShowModel
from text_window import TextWindow
from show_text import ShowText
from gpt_api import ChatGPT
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup
import package.live2d.v3 as live2d

live2d.init()
pygame.init()
pygame.mixer.init()

class VoiceRecognitionThread(QThread):
    result_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, recognizer):
        super().__init__()
        self.recognizer = recognizer

    def run(self):
        try:
            print("Listening...")

            # Capture audio using sounddevice
            duration = 8  # seconds
            fs = 16000  # Sample rate
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()  # Wait until recording is finished

            # Convert the NumPy array to AudioData
            audio_data = sr.AudioData(np.array(recording).tobytes(), fs, 2)

            # Recognize the audio using Google Web Speech API
            voice_input = self.recognizer.recognize_google(audio_data, language="zh-CN")
            print(f"Recognized voice input: {voice_input}")
            self.result_ready.emit(voice_input)

        except:
            pass

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

        # Set up speech recognition with sounddevice
        self.recognizer = sr.Recognizer()

        # Set up a timer to check the text_window.show_text attribute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_text_window)
        self.timer.start(1000)  # Check every 1 second

        # Create the voice recognition thread
        self.voice_thread = VoiceRecognitionThread(self.recognizer)
        self.voice_thread.result_ready.connect(self.handle_voice_result)
        self.voice_thread.error_occurred.connect(self.handle_voice_error)

    def check_text_window(self):
        show = self.text_window.get_text()

        # If there's text in the window, process it
        if show:
            result = self.chat.asking(show)
            self.play_response(result)

        # If there's no text in the window, start listening for voice input
        else:
            if not self.voice_thread.isRunning():
                self.voice_thread.start()

    def handle_voice_result(self, voice_input):
        if not pygame.mixer.get_busy():
            result = self.chat.asking(voice_input)
            self.play_response(result)

    def handle_voice_error(self, error_message):
        print(error_message)

    def play_response(self, text):
        tts = gTTS(text=text, lang='zh', slow=False)
        tts.save('./live_2d_model/hiyori_free_en/runtime/sounds/test.mp3')
        
        sound = AudioSegment.from_mp3("live_2d_model/hiyori_free_en/runtime/sounds/test.mp3")
        final = speedup(sound, playback_speed=1.25) 
        final.export("live_2d_model/hiyori_free_en/runtime/sounds/test.wav", format="wav")

        pygame.mixer.Sound('live_2d_model/hiyori_free_en/runtime/sounds/test.wav').play()

        if self.show_model.model.IsMotionFinished():
            self.show_model.model.StartMotion("Idle", 0, live2d.MotionPriority.FORCE.value)
            self.show_model.update() 

        self.show_text.updateText(text)

app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
