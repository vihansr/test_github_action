import os
import smtplib
import psycopg2
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_HOST")
SENDER_EMAIL = os.getenv("SENDER_MAIL")
SMTP_KEY = os.getenv("SMTP_KEY")


def fetch_subscribers():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT email FROM subscribers")
        emails = [row[0] for row in cur.fetchall()]
        conn.close()
        return emails
    except Exception as e:
        print(f"❌ Failed to connect to DB: {e}")
        return []


def send_test_email(to_email):
    try:
        msg = MIMEText("✅ This is a test email from GitHub Actions!")
        msg["Subject"] = "✅ Test Email from GitHub Actions"
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SMTP_KEY)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        print(f"📤 Sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed for {to_email}: {e}")


if __name__ == "__main__":
    print("🔍 Testing DB and SMTP environment variables...")
    emails = fetch_subscribers()
    if not emails:
        print("⚠️ No emails fetched.")
    for email in emails:
        send_test_email(email)
