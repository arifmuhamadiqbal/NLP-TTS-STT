import streamlit as st
from gtts import gTTS
import requests
from io import BytesIO
import speech_recognition as sr

# Fungsi untuk mengonversi teks ke suara (TTS)
def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    return audio_buffer.getvalue()

# Streamlit App
st.title('Speech Processing with Streamlit')

# Text-to-Speech (TTS)
st.header('Text-to-Speech (TTS)')
tts_text = st.text_area('Enter text for Text-to-Speech:', 'Hello, how are you?')
tts_language = st.selectbox('Select language:', ['en', 'es', 'fr', 'id'])
if st.button('Convert to Speech'):
    tts_audio = text_to_speech(tts_text, language=tts_language)
    st.audio(tts_audio, format='audio/wav', start_time=0)

# Speech-to-Text (STT)
st.header('Speech-to-Text (STT)')
st.info('Click the button to start real-time speech-to-text from your microphone.')

# Create a SpeechRecognition recognizer
recognizer = sr.Recognizer()

# Placeholder for the recognized text
text_result = ""

# Function to start the speech recognition
def start_listening():
    global text_result

    # Use the browser's microphone
    with sr.Microphone() as source:
        st.info("Listening...")

        try:
            # Adjust for ambient noise and recognize the speech
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source, timeout=10)

            # Perform speech-to-text
            text_result = recognizer.recognize_google(audio_data)

            st.success("Speech recognition completed!")

        except sr.UnknownValueError:
            st.warning("Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service: {e}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Button to start listening and convert to text
if st.button('Start Listening'):
    start_listening()

# Display the recognized text
st.subheader('Speech-to-Text Result:')
st.write(text_result)