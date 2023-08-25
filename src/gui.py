import sys
import matplotlib.pyplot as plt
import qdarkstyle
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from .audio_tools import AudioProcessor
from . import config, utils

class WaveformViewer(QWidget):
    def __init__(self):
        super().__init__()
        plt.style.use('ggplot')
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.reset_ax()
        
    def reset_ax(self):
        self.ax.clear()
        self.ax.set_xlabel('')
        self.ax.set_ylabel('')
        self.ax.set_axis_off()
        self.canvas.draw()

    def update_waveform(self, waveform_data):
        self.ax.clear()
        self.ax.plot(waveform_data, color='orange')
        self.ax.set_axis_off()
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.APPLICATION_TITLE)
        self.resize(*config.APPLICATION_SIZE)
        self.setMaximumSize(QtCore.QSize(*config.APPLICATION_SIZE))
        self._audio_processor = AudioProcessor()
        self._create_widgets()
        self._initialize_icons()
        self._create_layouts()
        self._define_buttons_handlers()
        self._define_thread_signals()

    def _define_thread_signals(self):
        self._audio_processor.playing_finished.connect(self.on_playing_finished)
        self._audio_processor.recording_finished.connect(self.on_recording_finished)

    def _define_buttons_handlers(self):
        self.play_button.clicked.connect(self.play_button_click)
        self.start_record_button.clicked.connect(self.start_record_button_click)
        self.stop_record_button.clicked.connect(self.stop_record_button_click)
        self.stop_record_button.setEnabled(False)

    def _create_layouts(self):
        self.layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.stop_record_button)
        self.buttons_layout.addWidget(self.start_record_button)
        self.buttons_layout.addWidget(self.play_button)
        self.layout.addWidget(self.waveform_viewer)
        self.layout.addLayout(self.buttons_layout)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def _create_widgets(self):
        self.waveform_viewer = WaveformViewer()
        self.play_button = QtWidgets.QPushButton(self)
        self.stop_record_button = QtWidgets.QPushButton(self)
        self.start_record_button = QtWidgets.QPushButton(self)
        self.play_button.setGeometry(QtCore.QRect(580, 290, 75, 24))
        self.stop_record_button.setGeometry(QtCore.QRect(50, 290, 75, 24))
        self.start_record_button.setGeometry(QtCore.QRect(100, 290, 75, 24))
        self.play_button.setFixedSize(32,32)
        self.start_record_button.setFixedSize(32,32)
        self.stop_record_button.setFixedSize(32,32)
        self.play_button.setToolTip("Play the last recorded audio")
        self.start_record_button.setToolTip("Start recording audio")
        self.stop_record_button.setToolTip("Stop recording audio")

    def _initialize_icons(self):
        self._main_icon = QtGui.QIcon()
        self._play_icon = QtGui.QIcon()
        self._pause_icon = QtGui.QIcon()
        self._start_record_icon = QtGui.QIcon()
        self._stop_record_icon = QtGui.QIcon()

        self._main_icon.addPixmap(QtGui.QPixmap(config.MAIN_ICON_FILE),
                            QtGui.QIcon.Normal, 
                            QtGui.QIcon.Off)
        self._play_icon.addPixmap(QtGui.QPixmap(config.PLAY_ICON_FILE), 
                            QtGui.QIcon.Normal, 
                            QtGui.QIcon.Off)
        self._pause_icon.addPixmap(QtGui.QPixmap(config.PAUSE_ICON_FILE),
                            QtGui.QIcon.Normal, 
                            QtGui.QIcon.Off)
        self._start_record_icon.addPixmap(QtGui.QPixmap(config.START_RECORD_ICON_FILE), 
                            QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
        self._stop_record_icon.addPixmap(QtGui.QPixmap(config.STOP_RECORD_ICON_FILE), 
                            QtGui.QIcon.Normal, 
                            QtGui.QIcon.Off)
        
        self.setWindowIcon(self._main_icon)
        self.play_button.setIcon(self._play_icon)
        self.start_record_button.setIcon(self._start_record_icon)
        self.stop_record_button.setIcon(self._stop_record_icon)
                                
    
    def reset_layout(self):
        self.play_button.setIcon(self._play_icon)
        self.play_button.setEnabled(True)
        self.start_record_button.setEnabled(True)
        self.stop_record_button.setEnabled(False)

    def stop_processor(self):
        self._audio_processor.stop_palying()
        self._audio_processor.stop_recording()

    def play_button_click(self):
        if self._audio_processor.is_playing:
            self.stop_processor()
            self.reset_layout()
        else:
            self.play_button.setIcon(self._pause_icon)
            self.start_record_button.setEnabled(False)
            self.stop_record_button.setEnabled(False)
            last_audio_file = utils.get_last_audio_file_name()
            if last_audio_file:
                self._audio_processor.start_playing(last_audio_file)
                waveform_data = self._audio_processor.playing_thread.audio_data
                self.waveform_viewer.update_waveform(waveform_data)  
            else:
                self.setWindowTitle(config.APPLICATION_TITLE + " File Not Found!")
                self.reset_layout()

    def start_record_button_click(self):
        file_path = utils.create_new_audio_file_name()
        self._audio_processor.start_recording(file_path)
        self.play_button.setEnabled(False)
        self.start_record_button.setEnabled(False)
        self.stop_record_button.setEnabled(True)
        
    def stop_record_button_click(self):
        self.stop_processor()
        self.reset_layout()

    def on_recording_finished(self):
        self.stop_processor()
        self.reset_layout()

    def on_playing_finished(self):
        self.stop_processor()
        self.reset_layout()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())

