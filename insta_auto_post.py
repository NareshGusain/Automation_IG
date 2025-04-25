import os
import json
import time
import schedule
from instagrapi import Client
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Load configuration
CONFIG_FILE = "config.json"
SESSION_FILE = "session.json"
VIDEO_FOLDER = "videos"
LOG_FILE = "log.txt"
START_PART = 6  # Start part number from 6

# Load Instagram credentials
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

USERNAME = config["username"]
PASSWORD = config["password"]

# Initialize Instagram Client
cl = Client()

# Try to load session to avoid OTP
if os.path.exists(SESSION_FILE):
    cl.load_settings(SESSION_FILE)
    try:
        cl.login(USERNAME, PASSWORD)
    except Exception:
        print("⚠ Session expired! Logging in again.")
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
else:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(SESSION_FILE)

# Function to get next part number
def get_next_part():
    if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        return START_PART

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        if not lines:  # Empty log file
            return START_PART

        last_line = lines[-1].strip()
        if "Part-" not in last_line:  # Safety check
            return START_PART

        try:
            last_part = int(last_line.split("Part-")[1].split(".")[0])
            return last_part + 1
        except (IndexError, ValueError):
            return START_PART  # Default to START_PART if error occurs

# Function to add only the part number **exactly next to "Part-"**
def add_part_number(video_path, part_number):
    clip = VideoFileClip(video_path)

    # Generate text clips
    part_text = TextClip("Part  ", fontsize=90, color='black', font="Lobster", method='caption')
    number_text = TextClip(f"{part_number}", fontsize=90, color='#CA0147', font="Lobster", method='caption')

    # Calculate exact positions
    part_x = clip.w * 0.34  # "Part-" position (left-side)
    number_x = part_x + part_text.w - 5  # Number placed just after "Part-"
    y_position = clip.h - 600  # Adjust height for better placement

    part_text = part_text.set_position((part_x, y_position)).set_duration(clip.duration)
    number_text = number_text.set_position((number_x, y_position)).set_duration(clip.duration)

    # Composite video with both text clips
    final_clip = CompositeVideoClip([clip, part_text, number_text])

    # Save new video
    output_path = os.path.join(VIDEO_FOLDER, f"Part-{part_number}.mp4")
    final_clip.write_videofile(output_path, codec="libx264", fps=clip.fps)

    clip.close()
    part_text.close()
    number_text.close()
    final_clip.close()

    return output_path

# Function to upload video
def upload_video():
    # Sort files numerically in ascending order
    files = sorted(
        [f for f in os.listdir(VIDEO_FOLDER) if f.endswith((".mp4", ".mov"))],
        key=lambda x: int(''.join(filter(str.isdigit, x)))  # Extract numbers from filenames
    )

    if not files:
        print("✅ No videos left to upload!")
        return

    video_file = files[0]
    video_path = os.path.join(VIDEO_FOLDER, video_file)

    # Get part number
    part_number = get_next_part()

    # Process video to add text overlay
    processed_video_path = add_part_number(video_path, part_number)

    # Load captions
    with open("captions.txt", "r") as f:
        captions = f.readlines()

    caption = captions[part_number % len(captions)].strip() if captions else "🎬 Enjoy this clip! #uncutframesx #entertainment #fun"

    # Upload video
    print(f"🚀 Uploading {processed_video_path}...")
    try:
        cl.video_upload(processed_video_path, caption)
        print(f"✅ Uploaded {processed_video_path}")

        # Log uploaded video
        with open(LOG_FILE, "a") as f:
            f.write(f"Part-{part_number}.mp4\n")

        # Delete original and processed video after upload
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(processed_video_path):
            os.remove(processed_video_path)
        print(f"🗑 Deleted {video_file} after upload.")

    except Exception as e:
        print(f"❌ Failed to upload {processed_video_path}: {e}")

# First upload starts immediately
upload_video()

# Schedule video uploads every 20 minutes
schedule.every(20).minutes.do(upload_video)

print("🚀 Auto-upload system started...")

while True:
    schedule.run_pending()
    time.sleep(10)