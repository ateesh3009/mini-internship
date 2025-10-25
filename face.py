import cv2
from deepface import DeepFace
import time

def map_emotion_to_label(dominant_emotion, emotion_prob):
    em = dominant_emotion.lower()
    if em == "happy":
        return "Happy"
    if em == "angry":
        return "Angry"
    if em == "sad":
        if emotion_prob >= 0.65:
            return "Crying"
        return "Sad"
    if em == "neutral":
        return "Feeling/Neutral"
    if em == "surprise":
        return "Surprised"
    if em == "fear":
        return "Fearful"
    if em == "disgust":
        return "Disgust"
    return dominant_emotion.capitalize()

def analyze_frame(frame, detector_backend="opencv"):
    results_for_frame = []
    try:
        objs = DeepFace.analyze(
            frame,
            actions=["emotion"],
            detector_backend=detector_backend,
            enforce_detection=False
        )
    except Exception as e:
        print("DeepFace analyze error:", e)
        return results_for_frame

    detections = objs if isinstance(objs, list) else [objs]

    for det in detections:
        region = det.get("region", {})
        if "x" not in region:
            continue
        x, y, w, h = region["x"], region["y"], region["w"], region["h"]
        dom_emotion = det.get("dominant_emotion", "neutral")
        emotion_probs = det.get("emotion", {})
        prob = emotion_probs.get(dom_emotion, 0)
        label = f"{map_emotion_to_label(dom_emotion, prob)} ({int(prob * 100)}%)"
        print(f"Emotion: {dom_emotion}, Probability: {prob}, Label: {label}")  # Debugging
        results_for_frame.append((x, y, w, h, label))
    return results_for_frame

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    last_analysis_time = 0
    analysis_interval = 1.0
    detector_backend = "opencv"

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        display = frame.copy()
        now = time.time()

        if now - last_analysis_time > analysis_interval:
            faces = analyze_frame(frame, detector_backend)
            last_analysis_time = now
        else:
            faces = []

        for (x, y, w, h, label) in faces:
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
            label_y = y - 10 if y - 10 > 10 else y + h + 20
            (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(display, (x, label_y - text_h - 8), (x + text_w + 10, label_y + 2), (0, 255, 0), -1)
            cv2.putText(display, label, (x + 5, label_y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        cv2.imshow("Live Emotion Detection", display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
