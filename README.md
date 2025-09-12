# 🚀 Scam/Fraud Keyword Detector

## 🎯 Objective
This project is a simple prototype designed to detect scam or fraud-related content in text messages, emails, or chats.  
The detection is performed in two ways:

- **Keyword/Regex-based detection**: Matches known scam-related phrases or patterns.
- **Machine Learning (ML) model**: Learns patterns from sample training data and predicts whether a given text is likely to be fraudulent.

The tool provides an easy-to-use **Streamlit web application** where users can input text and instantly see detection results.

---

## 🛠️ Tech Stack
- **Python 3.x** – Core programming language  
- **Streamlit** – For building the interactive web application  
- **Pandas** – Data preprocessing and handling training data  
- **Scikit-learn** – Machine Learning pipeline (vectorization + classification)  
- **Joblib** – Saving and loading trained ML models  
- **Regex (re)** – Rule-based keyword/regex matching  
- **Pydub + FFmpeg (optional)** – For handling audio input and converting to text  

---

## ⚙️ Setup Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Chenthil-Hari/web.git
   cd web
2.Install Dependencies pip install -r requirements.txt

3. Prepare Data & Train Model - Add training samples in sample_data.csv - Run training to process the dataset and generate the model/keywords: python src/train.py

4. Run the Streamlit Application streamlit run src/app_streamlit.py Open http://localhost:8501 in your browser to access the app. 
📊 Example Input: "This is a scam, click here!" 
Output: ⚠️ Scam keyword detected → 'scam' 


## Team Members:
• Team Leader: Ahilesh M 

• Members: 
- B S Chenthil Hari 
- Jyothika V
