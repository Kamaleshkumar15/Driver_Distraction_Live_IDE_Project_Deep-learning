import csv
import os
import time
from datetime import datetime

try:
    import winsound
except ImportError:
    winsound = None

class AlertManager:
    def __init__(self, log_file="logs/events.csv", cooldown=2.0):
        self.log_file = log_file
        self.cooldown = cooldown
        self.last = {}

        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        if not os.path.exists(log_file):
            with open(log_file, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(
                    ["timestamp", "event", "severity"]
                )

    def alert(self, event, severity="HIGH"):
        now = time.time()
        if now - self.last.get(event, 0) < self.cooldown:
            return

        self.last[event] = now

        with open(self.log_file, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                datetime.now().isoformat(timespec="seconds"),
                event,
                severity
            ])

        if winsound:
            try:
                winsound.Beep(1400, 180)
                winsound.Beep(1800, 180)
            except Exception:
                pass
        else:
            print("\a", end="")
