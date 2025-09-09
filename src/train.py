from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import nltk

HERE = Path(__file__).resolve().parent.parent
DATA_PATH = HERE / "sample_data.csv"
MODEL_DIR = HERE / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_FILE = MODEL_DIR / "pipeline.pkl"

# ensure nltk stopwords (TF-IDF uses stop words option in vectorizer)
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    df = df.dropna(subset=["text", "label"])
    return df

def train(random_state=42):
    df = load_data()
    X = df["text"].astype(str)
    y = df["label"].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1,2), stop_words="english")),
        ("clf", LogisticRegression(solver="liblinear", class_weight="balanced", max_iter=1000))
    ])

    print("Training model on", len(x_train), "examples...")
    pipeline.fit(x_train, y_train)

    preds = pipeline.predict(x_test)
    probs = pipeline.predict_proba(x_test)[:, 1]

    print("\\n--- Evaluation on test set ---")
    print(classification_report(y_test, preds))
    try:
        print("ROC AUC:", roc_auc_score(y_test, probs))
    except Exception:
        pass

    joblib.dump(pipeline, MODEL_FILE)
    print(f"Saved trained pipeline to {MODEL_FILE}")

if __name__ == "__main__":
    train()
