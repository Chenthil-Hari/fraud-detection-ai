import speech_recognition as sr
from detector import FraudDetector

def capture_and_detect():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    detector = FraudDetector()

    print("🎤 Listening... Speak something (Ctrl+C to stop)")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"📝 You said: {text}")
        result = detector.analyze(text)
        print("🔍 Detection Result:", result)
        return text, result
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return None, {"error": "unknown_audio"}
    except sr.RequestError as e:
        print(f"⚠️ Could not request results from Google API; {e}")
        return None, {"error": "request_failed", "details": str(e)}

if __name__ == "__main__":
    capture_and_detect()
