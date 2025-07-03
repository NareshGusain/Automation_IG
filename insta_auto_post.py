import os
import json
import schedule
import time
from datetime import datetime, timedelta
from instagrapi import Client

CONFIG_FILE = "config.json"
SESSION_FILE = "session.json"
VIDEO_FOLDER = "videos"
LOG_FILE = "log.txt"

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

USERNAME = config["username"]
PASSWORD = config["password"]

cl = Client()

# Remove session file to force fresh login
if os.path.exists(SESSION_FILE):
    os.remove(SESSION_FILE)

try:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(SESSION_FILE)
except Exception as e:
    print("Login failed:", e)
    exit(1)

def upload_video():
    files = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith((".mp4", ".mov"))]
    if not files:
        print("No videos left to upload!")
        return

    video_file = files[0]
    video_path = os.path.join(VIDEO_FOLDER, video_file)
    caption = "Enjoy this reel! #automation"

    print(f"Uploading {video_path}...")
    try:
        cl.video_upload(video_path, caption)
        print(f"Uploaded {video_path}")

        with open(LOG_FILE, "a") as f:
            f.write(f"{video_file}\n")

        # Do NOT delete the video file after upload

    except Exception as e:
        print(f"Failed to upload {video_path}: {e}")

# Schedule upload at 8 PM IST every day
def run_daily_8pm_ist():
    # Calculate UTC time for 8 PM IST (IST = UTC+5:30)
    now = datetime.utcnow()
    target = now.replace(hour=14, minute=30, second=0, microsecond=0)  # 20:00 IST = 14:30 UTC
    if now > target:
        target += timedelta(days=1)
    delay = (target - now).total_seconds()
    print(f"Waiting {int(delay)} seconds until next upload at 8 PM IST...")
    time.sleep(delay)
    while True:
        upload_video()
        # Wait 24 hours for the next upload
        time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    run_daily_8pm_ist()