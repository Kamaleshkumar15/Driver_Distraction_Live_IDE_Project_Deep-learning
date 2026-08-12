# 🚗 Driver Distraction Detection System — Live Laptop Camera

A Python-based **real-time Driver Monitoring System** that uses a laptop webcam to detect driver distraction, drowsiness, yawning, looking away, and optional mobile-phone usage.

<img src="https://www.image2url.com/r2/default/gifs/1786517639348-a8f4eb28-ed20-4717-b306-8b1ca0ff912b.gif" width="480" alt="Driver Distraction Detection Live Demo">

The project is designed to run directly from **Python IDLE on Windows** using OpenCV, MediaPipe Face Mesh, and optionally YOLOv7.

## 🎬 Live Demo

[▶️ Watch the Live Demo](https://jumpshare.com/s/qQlMx4n33hY2K1juoKH7)

> Click the link above to watch the project running in real time.

## ✨ What It Detects

* 🙂 Face present / missing
* 👁️ Eyes closed for a sustained period → **DROWSINESS**
* 👀 Looking away → **DISTRACTION**
* 😮 Yawning
* 📱 Cell phone → **YOLOv7 object detection** *(optional)*
* ⚠️ Combined warning detection
* 🔊 Immediate Windows beep alert
* 📝 Event logging
* 📊 Real-time FPS display
* 🟢 Green / 🟡 Yellow / 🔴 Red status indicators

> ⚠️ **Educational prototype only.** This system is not a certified automotive safety system and should not be used as the sole safety mechanism in a real vehicle.

---

## 🧠 System Architecture

```text
                ┌─────────────────┐
                │  Laptop Camera  │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │     OpenCV      │
                └────────┬────────┘
                         ↓
              ┌──────────────────────┐
              │ MediaPipe Face Mesh  │
              └──────────┬───────────┘
                         ↓
          ┌─────────────────────────────┐
          │ EAR / MAR / Gaze / Head     │
          │ Direction Analysis           │
          └──────────────┬──────────────┘
                         ↓
              ┌─────────────────────┐
              │ YOLOv7 Phone       │
              │ Detection (Optional)│
              └──────────┬──────────┘
                         ↓
              ┌─────────────────────┐
              │ Temporal Decision   │
              │ Logic               │
              └──────────┬──────────┘
                         ↓
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      🔊 Beep        ⚠️ Warning     📝 CSV Log
```

---

# 🚀 Run Directly from Python IDLE

## 1. Install Python

Install **Python 3.10 or Python 3.11**.

Recommended:

```text
Python 3.11
Windows 10 / Windows 11
```

## 2. Open Command Prompt

Navigate to the project folder:

```bash
cd path\to\Driver_Distraction_Live_IDE_Project
```

## 3. Install Dependencies

```bash
py -m pip install -r requirements.txt
```

If `py` is unavailable:

```bash
python -m pip install -r requirements.txt
```

## 4. Run Using IDLE

Open:

```text
run_project.py
```

with **Python IDLE**.

Then:

```text
F5 → Run Module
```

Allow camera permission if Windows asks.

## 5. Test the System

Try the following:

```text
👁️ Close your eyes for ~1.5 seconds
👀 Turn your head left/right
😮 Open your mouth for ~1 second
📱 Show a phone to the camera (if YOLOv7 is enabled)
```

Press:

```text
Q
```

to exit the camera window.

---

# 📱 YOLOv7 Phone Detection

The project can operate **without YOLOv7**.

Face monitoring features such as:

* Drowsiness
* Eye closure
* Yawning
* Looking away
* Head direction

can work without a YOLO model.

For mobile-phone detection, optionally add YOLOv7.

## Project Structure

```text
external/
└── yolov7/
```

Clone the official YOLOv7 repository:

```bash
git clone https://github.com/WongKinYiu/yolov7.git external/yolov7
```

Place the pretrained weights here:

```text
weights/
└── yolov7.pt
```

Then run:

```bash
python run_project.py
```

If YOLOv7 weights are unavailable, the application automatically continues with the facial-monitoring features and indicates that YOLO detection is disabled.

---

# 🖥️ Recommended Hardware

The project is designed for a normal laptop/desktop.

| Component        | Recommendation               |
| ---------------- | ---------------------------- |
| Operating System | Windows 10 / 11              |
| Python           | 3.10 / 3.11                  |
| RAM              | 8 GB or more                 |
| Camera           | 720p webcam                  |
| CPU              | Modern Intel / AMD processor |
| GPU              | Optional                     |
| IDE              | Python IDLE                  |

No Jupyter Notebook or Google Colab is required.

---

# 📂 Dataset

Custom YOLO dataset structure:

```text
data/
└── driver_dataset/
    ├── images/
    │   ├── train/
    │   └── val/
    │
    └── labels/
        ├── train/
        └── val/
```

## YOLO Label Format

Each annotation follows:

```text
class_id center_x center_y width height
```

All coordinates must be normalized between:

```text
0 and 1
```

## Suggested Classes

```text
0 attentive_driver
1 distracted_driver
2 drowsy_driver
3 phone_usage
4 yawning
5 looking_away
6 eating
7 drinking
```

---

# 🏋️ Training YOLOv7

The included:

```text
train_yolov7.py
```

acts as a launcher for the official YOLOv7 training script.

Example:

```bash
python train_yolov7.py --data data/driver_dataset/driver.yaml --weights weights/yolov7.pt --epochs 50
```

After training, run the monitoring system with the trained model:

```bash
python run_project.py --yolo-weights runs/train/exp/weights/best.pt
```

---

# ⚙️ Threshold Tuning

Detection thresholds can be configured in:

```text
src/config.py
```

Example:

```python
EYE_CLOSED_SECONDS = 1.5
LOOK_AWAY_SECONDS = 1.2
YAWN_SECONDS = 1.0
PHONE_CONFIRM_SECONDS = 0.4
```

### Reducing False Warnings

If the system generates too many warnings, increase the time thresholds.

For example:

```python
EYE_CLOSED_SECONDS = 2.0
LOOK_AWAY_SECONDS = 1.5
```

Longer thresholds require the condition to remain active for a longer period before triggering an alert.

---

# 🧩 Main Technologies

| Technology      | Purpose                         |
| --------------- | ------------------------------- |
| 🐍 Python       | Core programming                |
| 👁️ OpenCV      | Camera & image processing       |
| 🧠 MediaPipe    | Facial landmark detection       |
| 🤖 YOLOv7       | Optional phone/object detection |
| 📐 EAR          | Eye Aspect Ratio                |
| 👄 MAR          | Mouth Aspect Ratio              |
| 📊 CSV          | Event logging                   |
| 🔊 Windows Beep | Audio warning                   |

---

# 🔍 Detection Logic

### 😴 Drowsiness

The system monitors eye landmarks and calculates the **Eye Aspect Ratio (EAR)**.

If the eyes remain closed for a predefined duration:

```text
Eyes Closed
     ↓
Temporal Check
     ↓
DROWSINESS WARNING
```

### 👀 Looking Away

Facial landmarks are used to estimate approximate head/gaze direction.

```text
Normal Direction → SAFE
Left / Right     → DISTRACTION
```

### 😮 Yawning

Mouth landmarks are used to estimate the **Mouth Aspect Ratio (MAR)**.

If the mouth remains open for the configured duration:

```text
Mouth Open
    ↓
Temporal Check
    ↓
YAWNING DETECTED
```

### 📱 Phone Detection

YOLOv7 can optionally detect a mobile phone in the camera frame.

```text
Camera Frame
     ↓
YOLOv7
     ↓
Phone Detected
     ↓
Warning
```

---

# 🚨 Alert System

When a dangerous condition is detected, the system can provide:

```text
🔊 Windows Beep
⚠️ On-Screen Warning
📝 Event Log
📊 Detection Status
```

The interface uses different status levels:

```text
🟢 GREEN  → Normal
🟡 YELLOW → Attention
🔴 RED    → Warning
```

---

# 📝 Event Logging

Detected events can be recorded for later analysis.

Example:

```text
Timestamp, Event, Status
12:10:21, Eye Closed, DROWSINESS
12:10:25, Looking Away, DISTRACTION
12:10:30, Yawning, YAWNING
```

This makes it possible to review driver-monitoring events after testing.

---

# 📊 Real-Time Monitoring

The application displays:

* Camera feed
* Facial landmarks
* Detection status
* Warning messages
* FPS
* Optional YOLO bounding boxes
* Driver monitoring events

Everything runs in real time from the laptop webcam.

---

# 🎓 Project Presentation Points

## Dataset Overview

Driver images containing:

* Attentive driving
* Distracted driving
* Drowsiness
* Phone usage
* Yawning
* Looking away

with YOLO-format annotations.

## Model Setup

The system combines:

```text
YOLOv7
+
MediaPipe Face Mesh
+
Temporal Decision Logic
```

## Facial & Gesture Landmark Detection

The system analyzes:

* Eye landmarks
* Mouth landmarks
* Approximate gaze
* Head direction

## Distraction Logic

Different signals are converted into temporal events:

```text
Eye Closure
Looking Away
Yawning
Phone Usage
      ↓
Temporal Logic
      ↓
Driver Status
```

## Real-Time Monitoring

OpenCV provides the live camera interface with:

* Bounding boxes
* Labels
* Warnings
* FPS

## Alert System

The system provides:

```text
Visual Warning
+
Windows Beep
+
Event Logging
```

## Testing

Recommended test scenarios:

1. Normal attentive driving
2. Eye closure
3. Looking left/right
4. Yawning
5. Phone usage
6. Different lighting conditions
7. Different camera distances

---

# 📁 Project Structure

```text
Driver_Distraction_Live_IDE_Project/
│
├── run_project.py
├── train_yolov7.py
├── requirements.txt
├── README.md
│
├── src/
│   └── config.py
│
├── data/
│   └── driver_dataset/
│       ├── images/
│       │   ├── train/
│       │   └── val/
│       └── labels/
│           ├── train/
│           └── val/
│
├── weights/
│   └── yolov7.pt
│
├── external/
│   └── yolov7/
│
└── runs/
    └── train/
```

---

# 🎥 Demo

**Live project demonstration:**

👉 [Watch Driver Distraction Detection Demo](https://jumpshare.com/s/qQlMx4n33hY2K1juoKH7)

---

# ⚠️ Safety Notice

This project is an **educational and research prototype**.

It must **not** be used as the sole safety mechanism in a real vehicle.

Environmental conditions such as:

* Poor lighting
* Camera position
* Occlusion
* Facial appearance
* Camera quality
* Head position

can affect detection accuracy.

Always prioritize safe driving and never rely solely on this prototype for vehicle safety.

---

# 👨‍💻 Project

**Driver Distraction Detection System**

Built using:

**Python • OpenCV • MediaPipe • YOLOv7 • Computer Vision • Deep Learning**

⭐ If you find this project useful, consider giving the repository a **star** on GitHub!
