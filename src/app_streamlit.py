import streamlit as st
from pathlib import Path
import tempfile
import os
import sys

# allow src imports to work when running from repo root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT + "/src")

from detector import FraudDetector

# optional audio libs
HAS_AUDIO = True
try:
    import speech_recognition as sr
    from pydub import AudioSegment
except Exception:
    HAS_AUDIO = False

st.set_page_config(page_title="Fraud Detector Demo", layout="centered")
st.title("🚨 Fraud & Social Engineering Detector — Demo")

st.markdown(
    """
This demo analyzes text messages or short audio uploads for suspicious phrases and urgency patterns.
"""
)

try:
    detector = FraudDetector()
except Exception as e:
    st.error("Model not found. Please train the model first: `python -m src.train`\\nError: " + str(e))
    st.stop()

st.header("Analyze typed text")
text = st.text_area("Enter chat/call transcript (or type to simulate):", height=150)
col1, col2 = st.columns(2)
with col1:
    if st.button("Analyze Text"):
        if not text.strip():
            st.info("Enter some text to analyze.")
        else:
            res = detector.analyze(text)
            if res["flag"]:
                if res["source"] == "keyword":
                    st.warning("⚠️ Suspicious — keyword/regex match found!")
                    st.write("Matches:", res["matches"])
                else:
                    st.warning(f"⚠️ Suspicious — ML model flagged this message (score {res['ml_score']:.2f})")
            else:
                st.success("✔️ Looks safe (no keywords and ML score below threshold).")
            st.write("Full result:", res)

with col2:
    st.info("Try examples:\\n- 'Your account is suspended. Send OTP to reactivate.'\\n- 'Can you share the presentation deck?'\\n- 'Limited time investment opportunity, guaranteed returns.'")

st.write("---")
st.header("Audio upload (optional)")
st.write("Upload a short WAV/MP3 file. The app will transcribe then analyze the text (needs internet for Google STT).")

audio_file = st.file_uploader("Upload audio (wav, mp3, m4a, flac)", type=["wav", "mp3", "m4a", "flac"])
if audio_file is not None:
    if not HAS_AUDIO:
        st.error("Audio features require `SpeechRecognition` and `pydub` installed. See README.")
    else:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1])
        tfile.write(audio_file.read())
        tfile.flush()
        wav_path = tfile.name
        if not wav_path.lower().endswith(".wav"):
            try:
                sound = AudioSegment.from_file(wav_path)
                new_wav = wav_path + ".wav"
                sound.export(new_wav, format="wav")
                wav_path = new_wav
            except Exception as ex:
                st.error("Audio conversion failed: " + str(ex))
                wav_path = None
        if wav_path:
            r = sr.Recognizer()
            try:
                with sr.AudioFile(wav_path) as source:
                    audio = r.record(source)
                transcript = r.recognize_google(audio)
                st.subheader("Transcription")
                st.write(transcript)
                res = detector.analyze(transcript)
                if res["flag"]:
                    if res["source"] == "keyword":
                        st.warning("⚠️ Suspicious — keyword/regex match found in transcription.")
                        st.write("Matches:", res["matches"])
                    else:
                        st.warning(f"⚠️ Suspicious — ML flagged transcription (score {res['ml_score']:.2f})")
                else:
                    st.success("✔️ Transcription looks safe.")
                st.write("Full result:", res)
            except Exception as e:
                st.error("Transcription failed. (This demo uses Google STT which needs internet). Error: " + str(e))

st.write("---")
st.markdown("### Notes\\n- Keyword checks are strict: if a phrase matches, the message is flagged immediately.\\n- The ML model provides a fallback when no keywords match.")
