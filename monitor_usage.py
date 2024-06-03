import os
import smtplib
import psutil
import time
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import logging

# Configuration
TO_EMAIL = "david@1e26.com"
FROM_EMAIL = "david@1e26.com"
EMAIL_PASSWORD = "YOUR PASSWORD HERE"  # For Gmail, consider using an App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # or 465 for SSL
USAGE_THRESHOLD = 10  # Percentage
CHECK_INTERVAL = 60  # Seconds
LOW_USAGE_DURATION = 24 * 60 * 60  # 24 hours in seconds
LOG_FILE = '/home/ec2-user/monitoring/logfile.log'

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)


# Function to send an email
def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    except Exception as e:
        logging.error(f'Failed to send email: {e}')

# Function to check system usage
def check_usage():
    try: 
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        return cpu_usage, memory_usage
    except Exception as e:
        logging.error(f'Error checking system usage: {e}')
        return None, None

# Main monitoring loop
def monitor():
    low_usage_start = None

    while True:
        cpu_usage, memory_usage = check_usage()
        logging.info(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")

        if cpu_usage < USAGE_THRESHOLD and memory_usage < USAGE_THRESHOLD:
            if low_usage_start is None:
                low_usage_start = datetime.now()
            elif (datetime.now() - low_usage_start).total_seconds() > LOW_USAGE_DURATION:
                send_email(
                    "Low System Usage Alert",
                    f"The system has been on with low usage (CPU: {cpu_usage}%, Memory: {memory_usage}%) for more than 24 hours."
                )
                low_usage_start = None  # Reset after sending the email
                logging.info('Alert condition met and email sent.')

        else:
            low_usage_start = None  # Reset if usage goes above threshold

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    logging.info('Starting system usage monitor.')
    try:
        monitor()
    except Exception as e:
        logging.error(f'Script encountered an error: {e}')

