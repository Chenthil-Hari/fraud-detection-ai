Project README – AI for Real-Time Fraud & Social Engineering Detection
Objective
The objective of this project is to develop an AI-powered system that can analyze live text and audio conversations in real time to detect suspicious phrases, urgency cues, or fraudulent patterns. The system will provide alerts and warnings to financial institutions, customer support teams, and end-users to prevent financial fraud caused by social engineering attacks and scams.
Tech Stack
• Programming Languages: Python
Streamlit – web app interface
•  Pandas – data handling for training
•  Scikit-learn – ML pipeline (training & predictions)
•  Joblib – saving & loading ML models
•  Regex (re) – rule-based keyword detection
•  pydub + ffmpeg (optional) – audio-to-text preprocessing if needed

Setup Steps
1. Clone the Repository
git clone https://github.com/Chenthil-Hari/web.git
cd web
2. Install Dependencies
pip install -r requirements.txt
3. Prepare Data & Train Model
- Add training samples in sample_data.csv
- Run training to process the dataset and generate the model/keywords:
  python src/train.py
4. Run the Streamlit Application
streamlit run src/app_streamlit.py
Open http://localhost:8501 in your browser to access the app.
📊 Example
Input:  "This is a scam, click here!"
Output: ⚠️ Scam keyword detected → 'scam'

Team Members
• Team Leader: Ahilesh M
• Members:
   - B S Chenthil Hari
   - Jyothika V
