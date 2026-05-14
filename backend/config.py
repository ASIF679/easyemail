from dotenv import load_dotenv
import os 
load_dotenv()

class SMTPConfig:
    HOST     = os.getenv("SMTP_HOST")
    PORT     = int(os.getenv("SMTP_PORT", 587))
    USER     = os.getenv("SMTP_USER")
    PASSWORD = os.getenv("SMTP_PASSWORD")
    FROM     = os.getenv("SMTP_FROM_EMAIL")

smtp = SMTPConfig()