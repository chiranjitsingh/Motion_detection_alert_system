
import cv2
import numpy as np
import time
import os
from datetime import datetime
from twilio.rest import Client

# Twilio WhatsApp API Configuration
TWILIO_SID = "AC49a96e047a00af61c5fbc85e29a350e5"  # Replace with your Twilio SID
TWILIO_AUTH_TOKEN = "926525a3f55a66f0cf990059edb052ee"  # Replace with your Twilio Auth Token
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio Sandbox Number
RECIPIENT_WHATSAPP_NUMBER = "whatsapp:+919465516145"  # Replace with recipient's number

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Create the "recorded_videos" folder if it doesn't exist
RECORDINGS_FOLDER = "recorded_videos"
os.makedirs(RECORDINGS_FOLDER, exist_ok=True)

# Cooldown period for alerts (5 minutes = 300 seconds)
ALERT_COOLDOWN = 300
last_alert_time = 0

MOTION_RECORD_DURATION = 60  # Record for 60 seconds

def send_whatsapp_alert():
    """Send a WhatsApp alert message automatically using Twilio API."""
    global last_alert_time
    current_time = time.time()

    if current_time - last_alert_time > ALERT_COOLDOWN:
        last_alert_time = current_time  # Update last alert timestamp

        try:
            message = client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body="🚨 Alert! Motion detected in the surveillance area. Recording started.",
                to=RECIPIENT_WHATSAPP_NUMBER
            )
            print(f"✅ WhatsApp Alert Sent! Message SID: {message.sid}")
        except Exception as e:
            print("❌ Error sending WhatsApp alert:", e)

def motion_detection():
    """Motion detection function with automatic WhatsApp alerts and 1-minute video recording."""
    cap = cv2.VideoCapture(0)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    motion_detected = False
    video_writer = None
    video_filename = ""
    record_start_time = None  # Track recording start time

    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue  # Ignore small movements

            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if not motion_detected:
                motion_detected = True
                record_start_time = time.time()
                send_whatsapp_alert()  # Send alert when motion is detected

                # Store video inside "recorded_videos" folder
                video_filename = os.path.join(RECORDINGS_FOLDER, f"motion_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.avi")
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame1.shape[1], frame1.shape[0]))

        # Record video if motion detected
        if motion_detected and video_writer:
            video_writer.write(frame1)

            # Stop recording after 1 minute
            if time.time() - record_start_time > MOTION_RECORD_DURATION:
                motion_detected = False
                video_writer.release()
                print(f"🎥 Video saved: {video_filename}")

        cv2.imshow("Motion Detection", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(10) == 27:
            break

    if motion_detected and video_writer:
        video_writer.release()
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        motion_detection()
    except KeyboardInterrupt:
        print("🔴 Surveillance stopped.")
