import argparse
import time
import cv2

from src import config
from src.face_monitor import FaceMonitor, LEFT_EYE, RIGHT_EYE
from src.decision_engine import DecisionEngine
from src.alert_manager import AlertManager
from src.yolov7_detector import YOLOv7PhoneDetector

def text(frame, message, xy, scale=0.62, color=(255,255,255), thickness=2):
    cv2.putText(
        frame, message, xy, cv2.FONT_HERSHEY_SIMPLEX,
        scale, color, thickness, cv2.LINE_AA
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", type=int, default=config.CAMERA_INDEX)
    parser.add_argument("--yolo-weights", default="weights/yolov7.pt")
    parser.add_argument("--no-yolo", action="store_true")
    args = parser.parse_args()

    print("=" * 62)
    print(" DRIVER DISTRACTION DETECTION SYSTEM")
    print(" Live Laptop Camera | OpenCV + MediaPipe + YOLOv7")
    print("=" * 62)

    monitor = FaceMonitor(
        config.MAX_FACES,
        config.MIN_DETECTION_CONFIDENCE,
        config.MIN_TRACKING_CONFIDENCE
    )
    engine = DecisionEngine()
    alerts = AlertManager(
        "logs/events.csv",
        config.ALERT_COOLDOWN_SECONDS
    )

    yolo = YOLOv7PhoneDetector(
        args.yolo_weights,
        conf=config.YOLO_CONFIDENCE,
        iou=config.YOLO_IOU,
        img_size=config.YOLO_IMAGE_SIZE
    )
    if not args.no_yolo:
        yolo.setup()

    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    if not cap.isOpened():
        raise RuntimeError(
            "Camera could not be opened. Try --camera 1 or check Windows camera permission."
        )

    previous = time.time()
    fps = 0.0

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Could not read camera frame.")
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        # ---------------- YOLOv7 ----------------
        detections = yolo.detect(frame)
        phone_detected = False

        for det in detections:
            if det["label"].lower() in {
                "cell phone", "phone", "mobile phone"
            }:
                phone_detected = True
                x1,y1,x2,y2 = det["box"]

                cv2.rectangle(
                    frame, (x1,y1), (x2,y2),
                    (0,165,255), 3
                )
                text(
                    frame,
                    f"PHONE {det['confidence']:.0%}",
                    (x1, max(25, y1-10)),
                    color=(0,165,255)
                )

        # ---------------- Face Mesh ----------------
        result = monitor.process(frame)

        status = None

        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0].landmark

            x1,y1,x2,y2 = monitor.box(landmarks, w, h)
            cv2.rectangle(
                frame, (x1,y1), (x2,y2),
                (0,255,0), 3
            )
            text(
                frame, "FACE: DETECTED",
                (x1, max(25,y1-10)),
                color=(0,255,0)
            )

            left_ear = monitor.ear(landmarks, LEFT_EYE, w, h)
            right_ear = monitor.ear(landmarks, RIGHT_EYE, w, h)
            ear = (left_ear + right_ear) / 2

            mar = monitor.mar(landmarks, w, h)
            gaze = monitor.gaze_ratio(
                landmarks, LEFT_EYE, w, h
            )
            head = monitor.head_direction(landmarks, w, h)

            status = engine.update(
                ear, mar, gaze, head, phone_detected,
                config.EAR_THRESHOLD,
                config.MAR_THRESHOLD,
                config.GAZE_LEFT_THRESHOLD,
                config.GAZE_RIGHT_THRESHOLD,
                config.EYE_CLOSED_SECONDS,
                config.LOOK_AWAY_SECONDS,
                config.YAWN_SECONDS,
                config.PHONE_CONFIRM_SECONDS
            )

          
            lx = int(landmarks[33].x*w)
            rx = int(landmarks[263].x*w)
            top = int(min(landmarks[159].y, landmarks[386].y)*h)
            bottom = int(max(landmarks[145].y, landmarks[374].y)*h)
            cv2.rectangle(
                frame,
                (max(0,lx-10), max(0,top-10)),
                (min(w-1,rx+10), min(h-1,bottom+10)),
                (255,255,0), 2
            )

           
            text(frame, f"EAR: {ear:.2f}", (20, 35))
            text(frame, f"MAR: {mar:.2f}", (20, 65))
            text(frame, f"GAZE: {gaze:.2f}", (20, 95))
            text(frame, f"HEAD: {head}", (20, 125))

        else:
            status = {
                "drowsy": False,
                "looking_away": False,
                "yawning": False,
                "phone": phone_detected,
                "distracted": True,
                "messages": ["FACE NOT DETECTED"]
            }
            text(
                frame, "FACE: NOT DETECTED",
                (20, 40),
                color=(0,0,255)
            )

        # ---------------- Alerts ----------------
        for event in status["messages"]:
            if event == "FACE NOT DETECTED":
                continue
            alerts.alert(event)

        # ---------------- UI ----------------
        if status["distracted"]:
            cv2.rectangle(
                frame, (0, h-92), (w, h),
                (0,0,190), -1
            )
            warning = "WARNING: " + " + ".join(status["messages"])
            text(
                frame, warning,
                (20, h-55),
                scale=0.78,
                color=(255,255,255),
                thickness=2
            )
            text(
                frame, "ATTENTION REQUIRED!",
                (20, h-22),
                scale=0.55
            )
        else:
            cv2.rectangle(
                frame, (0, h-70), (w, h),
                (0,125,0), -1
            )
            text(
                frame, "DRIVER STATUS: ATTENTIVE",
                (20, h-28),
                scale=0.72
            )

       
        yolo_status = "YOLOv7: ACTIVE" if yolo.model else "YOLOv7: OFFLINE"
        text(
            frame, yolo_status,
            (w-260, 30),
            color=(0,255,255) if yolo.model else (180,180,180)
        )

    
        now = time.time()
        current_fps = 1.0 / max(now-previous, 1e-6)
        fps = current_fps if fps == 0 else (0.9*fps + 0.1*current_fps)
        previous = now

        text(frame, f"FPS: {fps:.1f}", (w-150, 60))
        text(frame, "Q = Quit", (w-150, 90), scale=0.5)

        cv2.imshow(
            "Driver Distraction Detection | LIVE Laptop Camera",
            frame
        )

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
