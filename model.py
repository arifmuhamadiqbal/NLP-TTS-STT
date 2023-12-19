from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import speech_recognition as sr
from flask_cors import CORS
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text', '')
    language = data.get('language', 'en')

    tts = gTTS(text=text, lang=language)
    tts.save("output.mp3")

    return send_file("output.mp3", as_attachment=True)

@app.route('/stt', methods=['POST'])
def speech_to_text():
    try:
        audio_file = request.files['audio']

        # Save the audio file to disk
        audio_file.save("temp_audio.wav")

        # Load the audio file
        audio = AudioSegment.from_file("temp_audio.wav")

        recognizer = sr.Recognizer()

        with sr.AudioFile("temp_audio.wav") as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)
        response = jsonify({'text': text})
        return response

    except sr.UnknownValueError:
        return jsonify({'error': 'Speech Recognition could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f"Could not request results from Google Speech Recognition service: {e}"}), 503
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000, threaded=True, host='0.0.0.0')

