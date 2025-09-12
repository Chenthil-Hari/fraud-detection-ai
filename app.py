import streamlit as st
from src.detector import FraudDetector
import speech_recognition as sr
import tempfile
import os
import sounddevice as sd
import soundfile as sf   # for saving audio

# Initialize detector
detector = FraudDetector()

st.set_page_config(page_title="Fraud Detection AI", page_icon="🔍", layout="wide")
st.title("🔍 Fraud Detection AI")

st.markdown("This app detects **fraudulent messages** using ML + keyword matching.")

# ---- Text Input ----
user_input = st.text_area("Enter a message or text to analyze:", "")

if st.button("Analyze Text"):
    if user_input.strip():
        result = detector.analyze(user_input)
        st.subheader("📊 Analysis Result")
        if result["flag"]:
            st.error(f"⚠️ Fraud Detected! (Source: {result['source']})")
        else:
            st.success("✅ No fraud detected.")
        st.json(result)
    else:
        st.warning("⚠️ Please enter some text.")

# ---- File Upload ----
uploaded_file = st.file_uploader("Or upload a text file", type=["txt"])
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    result = detector.analyze(text)
    st.subheader("📊 Analysis Result")
    st.json(result)

# ---- Live Audio ----
st.subheader("🎤 Live Audio Fraud Detection")

duration = st.slider("Recording duration (seconds)", 3, 15, 5)

if st.button("Start Recording"):
    st.info("Recording... Speak now!")
    recording = sd.rec(int(duration * 44100), samplerate=44100, channels=1, dtype="float32")
    sd.wait()
    st.success("✅ Recording complete!")

    # Save to temp WAV
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        sf.write(tmpfile.name, recording, 44100)
        tmp_path = tmpfile.name

    st.audio(tmp_path, format="audio/wav")

    # Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(tmp_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.write("📝 Transcribed Text:", text)
            result = detector.analyze(text)
            st.subheader("📊 Analysis Result")
            if result["flag"]:
                st.error(f"⚠️ Fraud Detected! (Source: {result['source']})")
            else:
                st.success("✅ No fraud detected.")
            st.json(result)
        except sr.UnknownValueError:
            st.warning("⚠️ Could not understand the audio.")
        except sr.RequestError:
            st.error("API error. Try again later.")
