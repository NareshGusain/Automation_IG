"""
📸 Instagram Reels Automation System using Meta API (Python)

This project is a complete Instagram Reels automation system built using Python and Meta's official Graph API.

🚀 Features:
-----------
✅ Automatically posts a reel every 20 minutes to the specified Instagram account.  
✅ Captions and thumbnails are auto-generated using smart logic.  
✅ Fully automated pipeline — no manual intervention once set up.  
✅ Secure login using account credentials provided in the config.  
✅ Ideal for content creators, marketers, and reel-based pages.

🛠️ Tech Stack:
--------------
- Python 🐍  
- Meta (Facebook/Instagram) Graph API  
- Scheduler (like `schedule` or `APScheduler`)  
- Thumbnail & Caption Generation Module (Custom-built)

🔧 How it works:
---------------
1. System reads Instagram account credentials from a secure config file.
2. Every 20 minutes, a reel is selected from a local/video directory.
3. Thumbnail is auto-generated from the video.
4. Caption is auto-generated based on the video metadata or AI-based logic.
5. Reel is uploaded to the account using Meta’s Graph API.

📂 Folder Structure:
-------------------
- `videos/` - Your raw reel videos  
- `thumbnails/` - Auto-generated thumbnails  
- `captions/` - Auto-generated captions  
- `config.py` - Secure credentials and settings  
- `reel_uploader.py` - Core logic for automation  
- `logs/` - Upload logs and error reports  

🔐 Important:
------------
This system requires valid Meta Developer credentials and an Instagram Business/Creator account connected to a Facebook Page.

📅 Scheduler:
------------
Reels are posted at a fixed interval of **20 minutes** using a Python scheduler.

📌 Note:
-------
- This system is built for educational and ethical usage only.
- Ensure you follow Instagram’s usage policies to avoid restrictions.

Feel free to fork this project and customize it to your needs!
"""
