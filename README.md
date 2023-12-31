

# Voice Recorder App

![alt text](https://github.com/alaeimo/VoiceRecorder/blob/master/src/icons/app.png)

This application is a simple Voice Recorder built using Python. It utilizes PyQt5, Python 3.10.9, and the sounddevice and soundfile libraries to provide audio recording functionality.

## How to Run

Follow these steps to run the application on your machine:

1. Install Python 3.10.

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure Alembic:
   Edit the alembic.ini file. Update the sqlalchemy.url parameter to your database URL:
   ```bash
   sqlalchemy.url = postgresql://username:password@localhost/voice_recorder
   ```

6. Configure SQLAlchemy:
  Edit the src/config.py file. Update the DATABASE_URL parameter to your database URL:
   ```bash
   DATABASE_URL = 'postgresql://username:password@localhost/voice_recorder'
   ```

7. Apply the migration to the database:
   Run the migration to apply the changes to the database:
   ```bash
   alembic upgrade head
   ```

8. Run the application:
   ```bash
   python app.py
   ```




The application will launch, allowing you to record and play audio files. Enjoy recording your audio with ease!

For more details, feel free to explore the code and make modifications according to your needs. If you encounter any issues or have suggestions, please don't hesitate to open an issue or pull request.
