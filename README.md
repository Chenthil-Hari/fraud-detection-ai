# Scam/Fraud Keyword Detector (Prototype)

This is a prototype that detects suspicious social engineering phrases using:
- Rule-based keywords & regex
- TF-IDF + LogisticRegression fallback
- Streamlit demo UI

## Project layout
sample_data.csv
models/
  - keywords.json
src/
  - train.py
  - detector.py
  - app_streamlit.py
requirements.txt
README.md

## Quick start (Git Bash)
1. Create & activate virtualenv
   python -m venv venv
   # Git Bash / Linux / macOS
   source venv/bin/activate
   # If using Windows PowerShell:
   # venv\\Scripts\\Activate.ps1

2. Install dependencies
   pip install -r requirements.txt

3. Train model
   python -m src.train

4. Run Streamlit demo
   streamlit run src/app_streamlit.py
   # If import errors occur, run:
   # PYTHONPATH=. streamlit run src/app_streamlit.py

## Notes
- Audio transcription uses Google Web Speech API (internet required). Install ffmpeg for audio conversion if needed.
- This is a demo/prototype only — not production-ready.
