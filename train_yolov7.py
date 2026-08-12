import argparse
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--weights", default="weights/yolov7.pt")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--img", type=int, default=640)
    args = parser.parse_args()

    repo = Path("external/yolov7")
    train_script = repo / "train.py"

    if not train_script.exists():
        raise FileNotFoundError(
            "YOLOv7 not found. Clone it into external/yolov7 first."
        )

    command = [
        "python", str(train_script),
        "--workers", "2",
        "--batch-size", str(args.batch),
        "--data", args.data,
        "--img-size", str(args.img),
        "--cfg", str(repo / "cfg/training/yolov7.yaml"),
        "--weights", args.weights,
        "--epochs", str(args.epochs)
    ]

    subprocess.run(command, check=True)

if __name__ == "__main__":
    main()
