import cv2
import time
import os
import pandas as pd
from datetime import datetime
from ultralytics import YOLO
from email_alert import send_email_alert
from telegram_alert import send_telegram_alert
import subprocess
import threading

# Load YOLOv8 model
print("[INFO] Loading YOLOv8 model...")
model = YOLO("yolov8s.pt")

# Settings
CONFIDENCE_THRESHOLD = 0.5
SUSPECT_CLASSES = ["knife", "gun", "cell phone"]
camera_location = {
    "latitude": 26.9124,
    "longitude": 75.7873,
    "address": "Lamrin Tech Skills University, Chandigarh Jalandhar Road, Boys Hostel , Ropar(Punjab)"
}

# Paths
os.makedirs("suspect_pics", exist_ok=True)
csv_path = "detection.csv"
if not os.path.exists(csv_path):
    pd.DataFrame(columns=["Time", "Label", "Confidence"]).to_csv(csv_path, index=False)

cap = cv2.VideoCapture(0)
cooldown = 5
last_alert_time = 0
last_sent_labels = set()

def trigger_alert(suspect_img_path, full_img_path, suspect_labels, timestamp):
    try:
        print("[BEEP] Playing sound alert...")
        subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"])

        print("[VOICE] Speaking alert in Hindi and English...")
        subprocess.run(['espeak', '-v', 'hi', "सावधान! आप की गतिविधि रिकॉर्ड हो रही है। पुलिस को सूचित किया जा चुका है!"])
        subprocess.run(['espeak', "Warning! Your activity is being recorded. Police have been notified."])

        print("[EMAIL] Sending email...")
        send_email_alert(
            full_img_path, suspect_img_path, suspect_labels, timestamp, camera_location
        )

        print("[TELEGRAM] Sending Telegram alert...")
        send_telegram_alert(
            full_img_path, suspect_img_path, suspect_labels, timestamp, camera_location
        )

    except Exception as e:
        print(f"[✖] Alert Thread Error: {e}")

print("[INFO] Starting CCTV... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to capture frame.")
        break

    results = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
    detections = results[0].boxes
    current_time = time.time()
    frame_copy = frame.copy()
    suspect_labels = []

    for box in detections:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls_id]

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        color = (0, 255, 0)

        if label in SUSPECT_CLASSES:
            color = (0, 0, 255)
            suspect_labels.append(label)
            print(f"\n\033[91m[DETECTED]\033[0m {label.upper()} with confidence {conf:.2f}")
        else:
            print(f"[INFO] Detected: {label} ({conf:.2f})")

        cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame_copy, f"{label.upper()} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    unique_suspects = set(suspect_labels)

    if unique_suspects and (current_time - last_alert_time) >= cooldown:
        if unique_suspects != last_sent_labels:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            suspect_img = f"suspect_pics/suspect_{timestamp}.jpg"
            full_img = f"suspect_pics/full_frame_{timestamp}.jpg"

            cv2.imwrite(suspect_img, frame_copy)
            cv2.imwrite(full_img, frame)
            print(f"[✔] Saved suspect image: {suspect_img}")
            print(f"[✔] Saved full frame image: {full_img}")

            df = pd.read_csv(csv_path)
            for label in unique_suspects:
                new_row = {"Time": timestamp, "Label": label, "Confidence": CONFIDENCE_THRESHOLD}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(csv_path, index=False)

            threading.Thread(target=trigger_alert, args=(
                suspect_img, full_img, list(unique_suspects), timestamp
            )).start()

            last_alert_time = current_time
            last_sent_labels = unique_suspects
        else:
            print("[INFO] Same suspects already alerted. Skipping...")
    elif suspect_labels:
        print("[INFO] Cooldown not yet passed, skipping alert...")

    cv2.imshow("Live CCTV Feed", frame_copy)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

