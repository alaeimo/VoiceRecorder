# https://icons8.com/icon/set/media-controls/flat-round
import os

basedir = os.path.dirname(os.path.abspath(__file__))
MAIN_ICON_FILE = os.path.join(basedir, "icons/voice_recorder.png")
PLAY_ICON_FILE = os.path.join(basedir, "icons/play.png")
PAUSE_ICON_FILE = os.path.join(basedir, "icons/pause.png")
START_RECORD_ICON_FILE = os.path.join(basedir, "icons/record.png")
STOP_RECORD_ICON_FILE = os.path.join(basedir, "icons/stop.png")
APPLICATION_TITLE = "Voice Recorder"
APPLICATION_SIZE = (664, 350)
RECORDED_FILES_PATH = os.path.join(os.path.dirname(basedir), "recordings")
if not os.path.exists(RECORDED_FILES_PATH):
    os.makedirs(RECORDED_FILES_PATH)
