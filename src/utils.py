from datetime import datetime
import os
from . import config

def create_new_audio_file_name():
    filename = "Recording_" + datetime.now().strftime("%Y-%m-%d-%I-%M-%S_") + ".wav"
    return os.path.join(config.RECORDED_FILES_PATH, filename)
     
def file_datetime(filename):
    if filename.startswith("Recording_") and filename.endswith(".wav"):
        timestamp_str = filename.split("_")[1]
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d-%I-%M-%S")
        return timestamp
    return None

def get_last_audio_file_name():
    list_of_files = os.listdir(config.RECORDED_FILES_PATH)
    list_of_audio_files = [filename for filename in list_of_files if filename.startswith("Recording_") and filename.endswith(".wav")]
    for filename in sorted(list_of_audio_files, key=file_datetime, reverse=True):
        return os.path.join(config.RECORDED_FILES_PATH, filename)
    return None