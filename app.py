import tempfile
from tempfile import NamedTemporaryFile
from flask import Flask, request, send_file, render_template
import openai 
import os
from dotenv import load_dotenv
import time
from pydub import AudioSegment
import json
import uuid
from flask_cors import CORS
import config

# Load environment variables from .env file
load_dotenv()


# Define function to convert Unicode to readable format and save to file
    

def save_transcription(transcription_text, save_dir):
    transcription_path = os.path.join(save_dir, 'transcription.txt')

    with open(transcription_path, 'w') as f:
        # f.write("WEBVTT\n\n")
        f.write(transcription_text)

    return transcription_path


# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(config)

# Set OpenAI API key
openai.api_key = app.config['OPENAI_API_KEY']
# Define endpoint to serve index.html
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})


@app.route("/")
def index():
    return render_template("index.html")

# Define endpoint to handle file upload and transcription


@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    # Get the uploaded file from the request
    file = request.files.get("audio")

    # Check if the file is an MP3 file
    if file.filename.endswith('.mp3'):
        # Start the timer
        start_time = time.time()

        # Load the input file using PyDub
        audio = AudioSegment.from_file(file)

        # Split the audio file into 10-minute segments
        segment_length = 5 * 60 * 1000  # 10 minutes in milliseconds
        audio_segments = []
        for i in range(0, len(audio), segment_length):
            segment = audio[i:i+segment_length]
            audio_segments.append(segment)

            # Export the segment to an MP3 file for debugging
            segment.export(os.path.join(
                app.config['TMP_AUDIO_FOLDER'], f'segment_{i}.mp3'), format='mp3')

        # Transcribe each audio segment using the Whisper API
        transcriptions = []
        for i, segment in enumerate(audio_segments):
            print(i)
            # Transcribe the audio using the OpenAI API
            with NamedTemporaryFile(suffix='.mp3') as temp_audio_file:
                segment.export(temp_audio_file.name, format='mp3')
                print(temp_audio_file.name)
                transcription = openai.Audio.transcribe(
                    "whisper-1", temp_audio_file, temperature=0, language='zh')
                print(transcription)
                # Save the transcription to a file
                save_path = os.path.join(
                    app.config['TMP_TEXT_FOLDER'], f'transcription_{i}.txt')
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(transcription['text'])

        # Combine all text files into a single file
        save_path = os.path.join(app.config['TMP_TEXT_FOLDER'], 'final.txt')
        with open(save_path, 'w', encoding='utf-8') as f:
            for i in range(len(audio_segments)):
                text_file_path = os.path.join(
                    app.config['TMP_TEXT_FOLDER'], f'transcription_{i}.txt')
                with open(text_file_path, 'r', encoding='utf-8') as tf:
                    f.write(tf.read())
                    f.write('\n\n')

        # End the timer
        end_time = time.time()

        # Calculate the execution time
        execution_time = end_time - start_time

        # Return a response with a link to download the transcription file
        return f"Transcription complete! Execution time: {execution_time} seconds. <a href='/download/transcription'>Download transcription</a>"
    else:
        return "Invalid file format. Supported format: MP3"


# Define endpoint to download transcription file
@app.route("/download/transcription")
def download():
    path = os.path.join(app.config['TMP_TEXT_FOLDER'], 'final.txt')
    download_name = "transcription_" + str(uuid.uuid4())
    return send_file(
        path,
        as_attachment=True,
        download_name=download_name,
        max_age=0
    )

# Define endpoint to return transcriptions as JSON


@app.route("/api/transcriptions")
def transcriptions():
    path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "tmp/texts/final.txt")
    with open(path, 'r') as f:
        transcription_text = f.read()
    transcriptions = transcription_text.split("\n")
    return json.dumps(transcriptions)


# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
