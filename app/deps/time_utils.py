from datetime import time, datetime
import pytz

def normalize_time(t: time) -> time:
    return time(hour=t.hour, minute=t.minute, second=t.second)

def convert_to_iso_utc(date_str: str, time_str: str, timezone_str: str = "Asia/Ho_Chi_Minh") -> str:
    # Merge day and time
    local_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")

    # Add local timezome
    local_timezone = pytz.timezone(timezone_str)
    localized_dt = local_timezone.localize(local_dt)

    # Convert to UTC
    utc_dt = localized_dt.astimezone(pytz.utc)

    # Return ISO format
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")