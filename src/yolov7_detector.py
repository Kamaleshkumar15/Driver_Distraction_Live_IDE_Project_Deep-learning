from pathlib import Path
import torch

class YOLOv7PhoneDetector:
    def __init__(self, weights, repo="external/yolov7",
                 conf=0.35, iou=0.45, img_size=640):
        self.weights = Path(weights)
        self.repo = Path(repo)
        self.conf = conf
        self.iou = iou
        self.img_size = img_size
        self.model = None

    def setup(self):
        if not self.weights.exists():
            print("[YOLOv7] weights/yolov7.pt not found.")
            print("[YOLOv7] Phone detection is disabled.")
            return False

        if not (self.repo / "hubconf.py").exists():
            print("[YOLOv7] external/yolov7 was not found.")
            print("[YOLOv7] Clone the official repository into external/yolov7.")
            return False

        try:
            self.model = torch.hub.load(
                str(self.repo),
                "custom",
                path=str(self.weights),
                source="local"
            )
            self.model.conf = self.conf
            self.model.iou = self.iou
            if torch.cuda.is_available():
                self.model.cuda()
            print("[YOLOv7] Loaded successfully.")
            return True
        except Exception as exc:
            print("[YOLOv7] Could not load model:", exc)
            return False

    def detect(self, frame):
        if self.model is None:
            return []

        results = self.model(frame, size=self.img_size)
        output = []

        for row in results.xyxy[0].detach().cpu().numpy():
            x1, y1, x2, y2, conf, cls = row
            cls = int(cls)
            names = self.model.names
            label = names[cls] if isinstance(names, dict) else names[cls]
            output.append({
                "box": (int(x1), int(y1), int(x2), int(y2)),
                "confidence": float(conf),
                "label": str(label)
            })
        return output
