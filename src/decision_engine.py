import time

class DecisionEngine:
    def __init__(self):
        self.start_times = {
            "drowsy": None,
            "looking_away": None,
            "yawning": None,
            "phone": None,
        }

    def sustained(self, name, condition, seconds):
        now = time.time()

        if condition:
            if self.start_times[name] is None:
                self.start_times[name] = now
            return (now - self.start_times[name]) >= seconds

        self.start_times[name] = None
        return False

    def update(self, ear, mar, gaze, head, phone,
               ear_threshold, mar_threshold,
               gaze_left, gaze_right,
               eye_seconds, look_seconds, yawn_seconds, phone_seconds):

        drowsy = self.sustained(
            "drowsy", ear < ear_threshold, eye_seconds
        )

        looking_away = self.sustained(
            "looking_away",
            gaze < gaze_left or gaze > gaze_right or head != "CENTER",
            look_seconds
        )

        yawning = self.sustained(
            "yawning", mar > mar_threshold, yawn_seconds
        )

        phone_use = self.sustained(
            "phone", phone, phone_seconds
        )

        active = []
        if drowsy:
            active.append("DROWSINESS")
        if looking_away:
            active.append("OFF ROAD")
        if yawning:
            active.append("YAWNING")
        if phone_use:
            active.append("PHONE")

        return {
            "drowsy": drowsy,
            "looking_away": looking_away,
            "yawning": yawning,
            "phone": phone_use,
            "distracted": len(active) > 0,
            "messages": active
        }
