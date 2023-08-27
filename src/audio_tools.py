import sounddevice as sd
import soundfile as sf
import time
from PyQt5 import QtCore
from pynput import keyboard
import queue

class RecorderThread(QtCore.QThread):
    recording_signal = QtCore.pyqtSignal(float)
    def __init__(self, file_path, samplerate=44100, channels=2):
        super().__init__()
        self.is_running = False
        self.file_path = file_path
        self.samplerate  = samplerate
        self.channels = channels

    def run(self):
        self.is_running = True
        q = queue.Queue()
        def callback(indata, frames, time, status):
            q.put(indata.copy())

        with sf.SoundFile(self.file_path, mode='x', samplerate=self.samplerate, channels=self.channels) as file:
            with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=callback):
                while self.is_running:
                    file.write(q.get())

    def stop(self):
        self.is_running = False
        sd.stop()
        self.wait()

class AudioPlayerThread(QtCore.QThread):
    play_signal = QtCore.pyqtSignal(float, float)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.is_playing = False
        self.load_audio()
    
    def load_audio(self):
        self.audio_data, self.sample_rate = sf.read(self.file_path)

    def run(self):
        start_time = time.time()
        if not self.is_playing:
            self.is_playing = True
            sd.play(self.audio_data, samplerate=self.sample_rate)
            info = sf.info(self.file_path)
            duration = info.duration
            while self.is_playing:
                elapsed_time = time.time() - start_time
                self.play_signal.emit(elapsed_time, duration)
                if elapsed_time >= len(self.audio_data) / self.sample_rate:
                    self.stop()
                    break
            self.play_signal.emit(duration, duration)
            self.is_playing = False

    def stop(self):
        self.is_playing = False
        sd.stop()

class AudioProcessor(QtCore.QObject):
    recording_finished = QtCore.pyqtSignal()
    playing_finished = QtCore.pyqtSignal()

    def __init__(self, on_playing_handler):
        super().__init__()
        self.on_playing_handler = on_playing_handler
        self.is_recording = False
        self.is_playing = False
        self.recording_thread = None
        self.playing_thread = None

    def start_recording(self, file_path):
        if not self.recording_thread or not self.recording_thread.isRunning():
            self.recording_thread = RecorderThread(file_path)
            self.recording_thread.finished.connect(self.recording_finished.emit)
            self.recording_thread.start()
            self.is_recording = True

    def stop_recording(self):
        if self.recording_thread:
            self.is_recording = False
            self.recording_thread.stop()

    def start_playing(self, file_path):
        if not self.playing_thread or not self.playing_thread.isRunning():
            self.playing_thread = AudioPlayerThread(file_path)
            self.playing_thread.finished.connect(self.playing_finished.emit)
            self.playing_thread.play_signal.connect(self.on_playing)
            self.playing_thread.start()
            self.is_playing = True

    def stop_palying(self):
        if self.playing_thread:
            self.is_playing = False
            self.playing_thread.stop()

    def on_playing(self, elapsed_time, duration):
        self.on_playing_handler(elapsed_time, duration)

class KeyInputThread(QtCore.QThread):
    key_press_signal = QtCore.pyqtSignal(keyboard.Key)
    def __init__(self):
        super().__init__()
        self.is_running = False

    def run(self):
        self.is_running = True
        def on_press(key):
            if key == keyboard.Key.page_up or key == keyboard.Key.page_down:
                self.key_press_signal.emit(key)
                
        with keyboard.Listener(on_press=on_press) as listener:
            while self.is_running:
                pass

    def stop(self):
        self.is_running = False
        self.stop()
        self.wait()

class KeyInputController(QtCore.QObject):
    def __init__(self, key_press_handler):
        super().__init__()
        self.key_press_handler = key_press_handler
        self.key_input_thread = KeyInputThread()
        self.key_input_thread.key_press_signal.connect(self.on_key_press)

    def start(self):
        self.key_input_thread.start()
    
    def on_key_press(self, key):
        self.key_press_handler(key)
    
    def stop(self):
        self.key_input_thread.stop()