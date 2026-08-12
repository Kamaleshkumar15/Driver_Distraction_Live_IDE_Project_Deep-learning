# 🚗 Driver Distraction Detection System

A Python deep-learning/vision project for running a **live Driver Monitoring System**. 

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces)

## 🎬 Live Demo

![Live Demo](Driver_Distraction_Live_Demo.jpg)

## 🌐 Online Hosting & Web Demo

To showcase this project online without requiring users to install Python locally, you can use the following methods:

### Option 1: Hugging Face Spaces (Recommended for Portfolios)
You can host this live on **Hugging Face Spaces** using **Gradio** or **Streamlit WebRTC**. 
1. Create a new Space on [Hugging Face](https://huggingface.co/spaces).
2. Choose **Gradio** or **Streamlit** as your SDK.
3. Modify the webcam input loop to use `streamlit-webrtc` (for Streamlit) or `gr.Image(source="webcam", streaming=True)` (for Gradio), which securely pipes the user's browser webcam to your cloud model.
4. Upload your `requirements.txt`, `yolov7.pt` (or a lighter model), and your python scripts.

### Option 2: Google Colab (Quick Testing)
Standard `cv2.VideoCapture(0)` does not work in Colab because the code runs on a cloud server, not your local machine. To run real-time inference in Colab:
1. Use Colab's custom JavaScript webcam snippets to capture frames from your browser.
2. Pass the base64 encoded images to your OpenCV/YOLO pipeline.
3. *See `colab_webcam_demo.ipynb` (if added to repo) for the exact implementation.*

---

## 🛠️ What it detects

*   **Face present / missing**
*   👁️ **Eyes closed** for a sustained period → DROWSINESS
*   👀 **Looking away** → DISTRACTION
*   😮 **Yawning**
*   📱 **Cell phone** → YOLOv7 object detector (optional weights)
*   **Combined warning**
*   🔊 **Immediate Windows beep** (Local execution only)
*   📝 **Event logging**
*   📊 **FPS**
*   🟢/🟡/🔴 **Green/yellow/red on-screen status**

> **Note:** Educational prototype only. It is not a certified automotive safety system.

## 🏗️ Architecture

Laptop Camera/Browser Webcam → OpenCV → MediaPipe Face Mesh → EAR / MAR / gaze / head direction → YOLOv7 phone detection → Temporal decision logic → Beep + warning + CSV log

## 💻 Run Locally (Directly from IDLE)

The program is deliberately written as normal Python scripts; there is no Jupyter/Colab requirement for local execution.

### Prerequisites
*   720p webcam
*   8 GB RAM or more
*   Windows 10/11
*   Python 3.10 or 3.11

### Installation Steps

1. Open Command Prompt in this folder.
2. Install dependencies:
   ```bash
   py -m pip install -r requirements.txt
