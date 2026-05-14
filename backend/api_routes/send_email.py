from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import smtp
from Schemas.email_request import EmailRequest

router = APIRouter()


def build_message(to_email: str, subject: str, body: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = smtp.FROM
    msg["To"]      = to_email
    msg.attach(MIMEText(body, "plain"))
    return msg


# ── Send endpoint ──────────────────────────────────────────────
@router.post("/send")
def send_emails(request: EmailRequest):

    if not request.emails:
        raise HTTPException(status_code=400, detail="No email addresses provided.")

    if not request.subject or not request.body:
        raise HTTPException(status_code=400, detail="Subject and body are required.")

    sent    = []
    failed  = []

    try:
        # Open ONE SMTP connection for the whole batch
        with smtplib.SMTP(smtp.HOST, smtp.PORT) as server:
            server.ehlo()
            server.starttls()          # TLS encryption
            server.ehlo()
            server.login(smtp.USER, smtp.PASSWORD)

            for email in request.emails:
                try:
                    msg = build_message(email, request.subject, request.body)
                    server.sendmail(smtp.FROM, email, msg.as_string())
                    sent.append(email)
                    print(f"✅ Sent → {email}")

                except Exception as e:
                    failed.append({"email": email, "reason": str(e)})
                    print(f"❌ Failed → {email} | {str(e)}")

                # Delay between sends to avoid spam filters
                time.sleep(request.delay)

    except smtplib.SMTPAuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="SMTP authentication failed. Check your email and App Password in .env"
        )
    except smtplib.SMTPConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to SMTP server {smtp.HOST}:{smtp.PORT}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SMTP error: {str(e)}")

    return {
        "total"        : len(request.emails),
        "sent_count"   : len(sent),
        "failed_count" : len(failed),
        "sent"         : sent,
        "failed"       : failed,
    }