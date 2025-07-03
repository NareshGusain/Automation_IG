"""
📸 Instagram Reels Automation System using Meta API (Python)

This project is an Instagram Reels automation system built using Python and Meta's official Graph API.

## 🚀 Features
- Automatically posts a reel every day at **8 PM IST** to the specified Instagram account.
- Fully automated pipeline — no manual intervention once set up.
- Secure login using account credentials provided in the config.
- Ideal for content creators, marketers, and reel-based pages.

## 🛠️ Tech Stack
- Python 🐍  
- Meta (Facebook/Instagram) Graph API  
- Scheduler (`schedule` library)

## 🔧 How it works
1. System reads Instagram account credentials from a secure config file (`config.json`).
2. Every day at 8 PM IST, the script selects the first video from the `videos/` directory.
3. The video is uploaded to the Instagram account using Meta’s Graph API.


## 📂 Folder Structure
- `videos/` - Your raw reel videos  
- `config.json` - Secure credentials and settings (not tracked in git, see below)  
- `insta_auto_post.py` - Core logic for automation  

## 🔐 Important
- This system requires valid Instagram credentials.

## 📅 Scheduler
Reels are posted **once daily at 8 PM IST** using a Python scheduler.

