from datetime import time

def normalize_time(t: time) -> time:
    return time(hour=t.hour, minute=t.minute, second=t.second)