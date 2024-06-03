import os
import smtplib
import psutil
import time
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# Configuration
TO_EMAIL = "david@1e26.com"
FROM_EMAIL = "david@1e26.com"
EMAIL_PASSWORD = "your_email_password"  # For Gmail, consider using an App Password
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587  # or 465 for SSL
USAGE_THRESHOLD = 10  # Percentage
CHECK_INTERVAL = 60  # Seconds
LOW_USAGE_DURATION = 24 * 60 * 60  # 24 hours in seconds

# Function to send an email
def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

# Function to check system usage
def check_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

# Main monitoring loop
def monitor():
    low_usage_start = None

    while True:
        cpu_usage, memory_usage = check_usage()
        print(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")

        if cpu_usage < USAGE_THRESHOLD and memory_usage < USAGE_THRESHOLD:
            if low_usage_start is None:
                low_usage_start = datetime.now()
            elif (datetime.now() - low_usage_start).total_seconds() > LOW_USAGE_DURATION:
                send_email(
                    "Low System Usage Alert",
                    f"The system has been on with low usage (CPU: {cpu_usage}%, Memory: {memory_usage}%) for more than 24 hours."
                )
                low_usage_start = None  # Reset after sending the email
        else:
            low_usage_start = None  # Reset if usage goes above threshold

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()

