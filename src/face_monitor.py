import cv2
import numpy as np
import mediapipe as mp


LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [61, 291, 13, 14]

class FaceMonitor:
    def __init__(self, max_faces=1, min_detection_confidence=0.55,
                 min_tracking_confidence=0.55):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=max_faces,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    @staticmethod
    def point(lm, w, h):
        return np.array([lm.x * w, lm.y * h], dtype=np.float32)

    def ear(self, landmarks, indices, w, h):
        p = [self.point(landmarks[i], w, h) for i in indices]
        horizontal = np.linalg.norm(p[0] - p[3])
        vertical = (
            np.linalg.norm(p[1] - p[5]) +
            np.linalg.norm(p[2] - p[4])
        ) / 2.0
        return float(vertical / (horizontal + 1e-6))

    def mar(self, landmarks, w, h):
        p1 = self.point(landmarks[MOUTH[0]], w, h)
        p2 = self.point(landmarks[MOUTH[1]], w, h)
        p3 = self.point(landmarks[MOUTH[2]], w, h)
        p4 = self.point(landmarks[MOUTH[3]], w, h)
        return float(np.linalg.norm(p3-p4) / (np.linalg.norm(p1-p2)+1e-6))

    def gaze_ratio(self, landmarks, eye_indices, w, h):

        p = [self.point(landmarks[i], w, h) for i in eye_indices]
        left = min(x[0] for x in p)
        right = max(x[0] for x in p)
        center = np.mean(p, axis=0)
        return float((center[0]-left) / (right-left+1e-6))

    def head_direction(self, landmarks, w, h):
        nose = self.point(landmarks[1], w, h)
        left = self.point(landmarks[33], w, h)
        right = self.point(landmarks[263], w, h)
        center = (left + right) / 2.0
        face_width = np.linalg.norm(right-left) + 1e-6
        dx = (nose[0]-center[0]) / face_width

        if dx < -0.16:
            return "LEFT"
        if dx > 0.16:
            return "RIGHT"
        return "CENTER"

    def box(self, landmarks, w, h):
        xs = [lm.x*w for lm in landmarks]
        ys = [lm.y*h for lm in landmarks]
        return (
            max(0, int(min(xs))),
            max(0, int(min(ys))),
            min(w-1, int(max(xs))),
            min(h-1, int(max(ys)))
        )

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.mesh.process(rgb)
