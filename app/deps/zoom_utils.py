import httpx

from app.core.config import settings

ZOOM_ACCOUNT_ID = settings.ZOOM_ACCOUNT_ID
ZOOM_CLIENT_ID = settings.ZOOM_CLIENT_ID
ZOOM_CLIENT_SECRET = settings.ZOOM_CLIENT_SECRET

async def get_zoom_access_token():
    url = "https://zoom.us/oauth/token"
    params = {
        "grant_type": "account_credentials",
        "account_id": ZOOM_ACCOUNT_ID,
    }
    auth = (ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, params=params, auth=auth)
        response.raise_for_status()
        return response.json()["access_token"]

# async def create_zoom_meeting(user_id: str, topic: str, start_time: str, duration: int = 40):
async def create_zoom_meeting(user_id: str, topic: str):
    token = await get_zoom_access_token()
    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "topic": topic,
        "type": 1,  # Instant Meeting
        # "type": 2,  # Scheduled Meeting
        # "start_time": start_time,  # ISO format: '2025-05-23T10:00:00Z'
        # "duration": duration,  # in minutes
        "timezone": "Asia/Ho_Chi_Minh",
        "settings": {
            "auto_recording": "local",
            "join_before_host": True,
            "participant_video": True,
            "host_video": True,
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()