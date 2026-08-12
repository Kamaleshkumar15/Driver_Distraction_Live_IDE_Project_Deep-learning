# 🚗 Driver Distraction Detection System — Live Laptop Camera

A Python deep-learning/vision project for running a **live Driver Monitoring System from a laptop webcam in IDLE**.
## 🎬 Live Demo
https://www.mdpi.com/2071-1050/16/17/7642
https://www.samsara.com/uk/blog/drowsiness-detection
https://imagevision.ai/applications/distracted-driver-detection/


## What it detects

- Face present / missing
- 👁️ Eyes closed for a sustained period → DROWSINESS
- 👀 Looking away → DISTRACTION
- 😮 Yawning
- 📱 Cell phone → YOLOv7 object detector (optional weights)
- Combined warning
- 🔊 Immediate Windows beep
- 📝 Event logging
- 📊 FPS
- Green/yellow/red on-screen status

> Educational prototype only. It is not a certified automotive safety system.

## Architecture

Laptop Camera
→ OpenCV
→ MediaPipe Face Mesh
→ EAR / MAR / gaze / head direction
→ YOLOv7 phone detection
→ temporal decision logic
→ beep + warning + CSV log

## Run directly from IDLE

1. Install Python 3.10 or 3.11.
2. Open Command Prompt in this folder.
3. Install:

```bash
py -m pip install -r requirements.txt
```

If `py` is unavailable:

```bash
python -m pip install -r requirements.txt
```

4. Open `run_project.py` in **IDLE**.
5. Press **F5 → Run Module**.
6. Allow camera permission if Windows asks.
7. Look at the camera and test:
   - close your eyes for ~1.5 seconds
   - turn your head left/right
   - open your mouth for ~1 second
   - optionally show a phone to the camera

Press **Q** in the camera window to exit.

## IMPORTANT: YOLOv7

The project works for face/eyes/drowsiness/yawning/head direction without a YOLO model.

For phone detection with YOLOv7:

```text
external/
└── yolov7/
```

Clone YOLOv7:

```bash
git clone https://github.com/WongKinYiu/yolov7.git external/yolov7
```

Put the pretrained `yolov7.pt` file in:

```text
weights/yolov7.pt
```

Then run:

```bash
python run_project.py
```

If weights are absent, the application automatically continues with the facial monitoring features and tells you that YOLO is disabled.

## IDLE settings

The program is deliberately written as normal Python scripts; there is no Jupyter/Colab requirement.

Recommended laptop:
- 720p webcam
- 8 GB RAM or more
- Windows 10/11
- Python 3.10/3.11

## Dataset

Custom YOLO dataset:

```text
data/driver_dataset/
├── images/
│   ├── train/
│   └── val/
└── labels/
    ├── train/
    └── val/
```

YOLO label:

```text
class_id center_x center_y width height
```

Normalized values must be between 0 and 1.

Suggested custom classes:

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

## Training

The included `train_yolov7.py` is a launcher for the official YOLOv7 training script.

Example:

```bash
python train_yolov7.py --data data/driver_dataset/driver.yaml --weights weights/yolov7.pt --epochs 50
```

Then run:

```bash
python run_project.py --yolo-weights runs/train/exp/weights/best.pt
```

## Threshold tuning

Open:

```text
src/config.py
```

Useful values:

```python
EYE_CLOSED_SECONDS = 1.5
LOOK_AWAY_SECONDS = 1.2
YAWN_SECONDS = 1.0
PHONE_CONFIRM_SECONDS = 0.4
```

If the system produces too many warnings, increase the time thresholds.

## Project presentation points

### Dataset Overview
Driver images with attentive/distracted/drowsy/phone/yawning/looking-away classes and YOLO annotations.

### Model Setup
YOLOv7 for object detection + MediaPipe Face Mesh for facial landmarks + temporal decision logic.

### Facial & Gesture Landmark Detection
Eye landmarks, mouth landmarks, approximate gaze and head direction.

### Distraction Logic
Phone use, yawning, drowsiness and looking away are converted into temporal events.

### Real-Time Monitoring
OpenCV webcam feed, bounding boxes, labels and FPS.

### Alert System
Windows beep + visual warning + event logging.

### Testing
Test safe driving, eye closure, head turning, yawning, lighting and camera distance.

## Safety

Do not use this prototype as the sole safety mechanism in a real vehicle.
