Motion Detection System with WhatsApp Alerts 🚨
Overview
This is a Python-based Motion Detection System using OpenCV that:
✔ Detects motion in a surveillance area
✔ Sends WhatsApp alerts using Twilio API
✔ Records video footage when motion is detected

🔧 Features
📷 Real-time motion detection using OpenCV

🚀 WhatsApp alerts sent automatically via Twilio

🎥 Records video when motion is detected

⏳ Configurable settings (sensitivity, recording time, cooldown, etc.)

🛠 Setup Instructions
1️⃣ Install Dependencies
Make sure you have Python installed, then install required packages:

bash
Copy
Edit
pip install opencv-python numpy python-dotenv twilio
2️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/motion-detection-system.git
cd motion-detection-system
3️⃣ Configure Environment Variables
Create a .env file in the project directory and add:

ini
Copy
Edit
# Twilio WhatsApp API Configuration
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
RECIPIENT_WHATSAPP_NUMBER=whatsapp:+919XXXXXXXXX

# Motion Detection Settings
ALERT_COOLDOWN=300  # Cooldown time (seconds) between alerts
MOTION_RECORD_DURATION=60  # Video recording duration (seconds)
⚠ Do not share your .env file! Add it to .gitignore

bash
Copy
Edit
echo ".env" >> .gitignore
🚀 Running the System
Run the motion detection script:

bash
Copy
Edit
python motion_detection.py
Press Esc to exit.

🛠 How It Works
The program continuously monitors for motion.

If motion is detected:

A WhatsApp alert is sent

A recording starts (default: 60 seconds)

The video is saved in the recorded_videos/ folder.

📂 Project Structure
bash
Copy
Edit
motion-detection-system/
│── recorded_videos/      # Folder to store recorded videos
│── motion_detection.py   # Main script for motion detection
│── .env                  # Environment variables (not pushed to GitHub)
│── .gitignore            # Ignore .env and unnecessary files
│── README.md             # Project documentation
🛠 Future Improvements
📡 Email Alerts (SMTP integration)

🤖 AI-based Object Recognition

📊 Web Dashboard to Monitor Alerts & Videos

📜 License
This project is open-source and available under the MIT License.
