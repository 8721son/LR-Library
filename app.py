import os
from flask import Flask, Response, request, jsonify
from flask_restful import Resource, Api
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)
api = Api(app)
r = sr.Recognizer()

@app.route("/")
def index():
    return "index"

@app.route('/stt',methods=['POST'])
def stt() :
    audio = request.files['file']
    wav_filename = "converted.wav"
    track = AudioSegment.from_file(audio,  format= 'm4a')
    file_handle = track.export(wav_filename, format='wav')
    msg = {
        'text' : speech_to_text(file_handle)
    }
    os.remove('converted.wav')
    return jsonify(msg),200

def speech_to_text(file) : 
    harvard = sr.AudioFile(file)
    with harvard as source:
        audio = r.record(source)
        return r.recognize_google(audio, language="ko-KR")

if __name__ == '__main__':
    app.run(debug=True)

