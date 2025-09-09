from pathlib import Path
import joblib
import json
import re

HERE = Path(__file__).resolve().parent.parent
MODEL_FILE = HERE / "models" / "pipeline.pkl"
KEYWORDS_FILE = HERE / "models" / "keywords.json"

class FraudDetector:
    def __init__(self, model_path=None, keywords_path=None, ml_threshold=0.5):
        self.model_path = Path(model_path) if model_path else MODEL_FILE
        self.keywords_path = Path(keywords_path) if keywords_path else KEYWORDS_FILE
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}. Run training (python -m src.train).")
        self.pipeline = joblib.load(self.model_path)

        with open(self.keywords_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.phrases = [p.lower() for p in data.get("phrases", [])]
        self.regexes = [re.compile(r, flags=re.IGNORECASE) for r in data.get("regex", [])]
        self.threshold = float(ml_threshold)

    def find_keyword_matches(self, text):
        text_l = text.lower()
        matches = []
        for p in self.phrases:
            if p in text_l:
                matches.append({"type": "phrase", "match": p})
        for rx in self.regexes:
            m = rx.search(text)
            if m:
                matches.append({"type": "regex", "match": m.group(0)})
        return matches

    def ml_score(self, text):
        prob = float(self.pipeline.predict_proba([text])[0][1])
        label = 1 if prob >= self.threshold else 0
        return label, prob

    def analyze(self, text):
        text = str(text).strip()
        matches = self.find_keyword_matches(text)
        if matches:
            return {
                "flag": True,
                "source": "keyword",
                "matches": matches,
                "ml_score": None
            }
        ml_label, ml_prob = self.ml_score(text)
        return {
            "flag": True if ml_label == 1 else False,
            "source": "ml" if ml_label == 1 else "ml_ok",
            "matches": matches,
            "ml_score": ml_prob
        }

if __name__ == "__main__":
    d = FraudDetector()
    print(d.analyze("Please send OTP 123456 to verify your account"))
    print(d.analyze("Let's meet tomorrow at the cafe."))
