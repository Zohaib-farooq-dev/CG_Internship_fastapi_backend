from app.core.celery import celery_app
import smtplib
from email.mime.text import MIMEText
import os

@celery_app.task
def send_patient_created_email(doctor_email: str, patient_id: int):
    print("invoking celery task email sending function")
    msg = MIMEText(f"A new patient (ID: {patient_id}) was created.")
    msg["Subject"] = "New Patient Created"
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = doctor_email

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        smtp.send_message(msg)
