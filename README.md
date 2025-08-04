# 💣 WhatsApp Message Bomber (Python + Selenium)

A Python automation script that sends repeated messages to a WhatsApp number using Selenium and a saved session. This is intended **only for educational and testing purposes**.

---

## 🚀 Features

- Automated message sending on WhatsApp Web.
- Uses Chrome browser with a persistent session (no need to scan QR every time).
- Configurable message, count, and delay.
- Robust handling of input box loading using multiple XPaths.
- Auto-installs compatible ChromeDriver via `webdriver-manager`.

---

## 📁 Folder Structure

📂 chrome_profile/
📂 WhatsAppProfile/
📂 WhatsAppSession/
📄 Bombing.py
📄 PyWhatKit_DB.txt



---

## 📥 Download

🔗 **Google Drive (project source & files):**  
[Click here to access](https://drive.google.com/drive/folders/1AXUZLNqzjeeRm62XDR2teTX7Ab3OoZ-_?usp=drive_link)

---

## 🔧 Requirements

- Python 3.x
- Google Chrome installed
- `pip install` the following:

```bash
pip install selenium webdriver-manager


⚙ Configuration (inside Bombing.py)
python
Copy
Edit
PHONE_NUMBER = "+91xxxxxxxxxx"        # Recipient phone number with country code
MESSAGE_TEXT = "..."                  # Message to be sent
MESSAGE_COUNT = 100                   # Number of messages
DELAY_BETWEEN_MESSAGES = 3           # Delay between messages (in seconds)
CHROME_PROFILE_PATH = "WhatsAppSession"  # Session folder for Chrome profile


💡 How to Use
Clone this repo or download from the Drive link.

Open terminal in the project folder.

Run the script:

bash

python Bombing.py

On first run, scan the QR code on WhatsApp Web.

Messages will begin sending once login is successful.


🛑 Disclaimer
⚠️ This project is for educational purposes only. Do not use this tool to spam or harass others. Abusing WhatsApp’s platform can result in account bans or legal consequences.

🧠 Author Notes
Tested with latest Chrome + Windows 10
Selenium uses persistent profile to avoid repeated QR scan
Includes fallback logic for locating message input box (helps avoid XPath issues)



