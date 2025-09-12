import streamlit as st
from src.detector import FraudDetector
from audiorecorder import audiorecorder
import speech_recognition as sr
import tempfile
import os

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
audio = audiorecorder("Start Recording", "Stop Recording")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        audio.export(tmpfile.name, format="wav")
        tmp_path = tmpfile.name

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
