# Guardian-Eye
my project is an AI-powered smart surveillance system that connects with CCTV cameras and automatically detects weapons like guns or knives in real-time. When a threat is detected, it instantly sends an emergency alert with the shop’s location and details (like number of intruders and weapons) to the nearest police or security personnel. 

#######Folder Structure--------------------------------------

guardian-eye/
│── detect_objects.py        # Main script for CCTV monitoring + YOLO detection
│── email_alert.py           # Module for sending email alerts
│── telegram_alert.py        # Module for sending Telegram alerts
│── requirements.txt         # Python dependencies
│── README.md                # Project documentation
│── yolov8s.pt               # YOLOv8 pretrained model weights (download separately)
│
├── suspect_pics/            # Stores cropped suspect images & full frame snapshots
│    ├── suspect_2025-08-22_23-45-11.jpg
│    ├── frame_2025-08-22_23-45-11.jpg
│    └── ...
│
├── logs/                    # (Optional) For storing logs or backup CSV files
│    └── detection.csv       # CSV log of all detections with timestamp & object details
│
└── config/                  # Configuration files (optional future use)
     └── camera_location.json


## 📌 Overview

Guardian Eye is an **AI-powered smart surveillance system** that connects with CCTV cameras and automatically detects **weapons (like guns or knives) and theft-related suspicious objects** in real time.
When a threat is detected, it:

* Draws bounding boxes on CCTV feed
* Plays alarm + warning voice (Hindi & English)
* Sends instant alerts with location and images via **Email & Telegram**

This system helps shops, malls, hospitals, and offices **prevent robbery and improve safety**.

---

## 🛠️ Tech Stack

* **YOLOv8 (Ultralytics)** → Object detection
* **OpenCV** → Video capture & frame processing
* **Python (3.9+)** → Core programming language
* **Pandas** → Logging detection details into CSV
* **SMTP / Gmail API** → Email alerts
* **Telegram Bot API** → Telegram alerts with images & location
* **espeak & paplay** → Voice warnings + beep sound

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/your-username/guardian-eye.git
cd guardian-eye
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> Example `requirements.txt`:

```
ultralytics==8.0.196
opencv-python
pandas
requests
```

### 4. Download YOLOv8 Model Weights

You need the pretrained YOLOv8 small model:

```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt
```

Place `yolov8s.pt` in your **project root folder** (same place as `detect_objects.py`).

### 5. Configure Alerts

* **Email** → Open `email_alert.py` and add your Gmail + App Password.
* **Telegram** → Open `telegram_alert.py` and add your Bot Token + Chat ID.

### 6. Run Detection

```bash
python detect_objects.py
```

---

## ✨ Features

✅ Real-time CCTV feed monitoring
✅ Detects **knife, gun, mobile phone** (can be extended)
✅ Red bounding box + label display on live video
✅ Plays **beep** + speaks Hindi & English warning
✅ Sends **Email alerts** (with images + Google Maps location)
✅ Sends **Telegram alerts** (cropped suspect image + full frame + details)
✅ Saves cropped suspects + full frame in `suspect_pics/`
✅ Logs all detections into `detection.csv` with timestamp & object details
✅ **5-second cooldown** (avoids spam alerts)
✅ **Multi-threaded alerts** (video doesn’t freeze while sending email/Telegram)

---

## 🔄 Technical Workflow

1. **Video Feed Capture** → CCTV or webcam using OpenCV
2. **YOLOv8 Detection** → Detects objects (knife, gun, phone, etc.) in each frame
3. **Bounding Boxes** → Drawn on suspicious items with labels
4. **Event Trigger** (if weapon detected):

   * Play beep + voice warning
   * Save suspect + full frame images
   * Log details in CSV
   * Send alerts via Email & Telegram
5. **Alerts Include**:

   * Timestamp
   * Suspect items
   * Images (cropped + full frame)
   * Camera location + Google Maps link

---

## 🚀 Scalability & Usability

* Can be deployed in **shops, schools, hospitals, banks, offices**
* Supports multiple CCTV cameras (can be extended)
* Future improvements:

  * Cloud integration for storage & monitoring
  * Mobile app for instant alerts
  * More object categories (explosives, suspicious behavior, etc.)

---

👉 Daddy, do you also want me to include a **“Project Structure” section** (folder tree with `detect_objects.py`, `email_alert.py`, `telegram_alert.py`, `suspect_pics/`, etc.) in README so others know where each file goes?
