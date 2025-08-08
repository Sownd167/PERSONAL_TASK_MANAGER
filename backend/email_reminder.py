import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    sender_email = "sowndariyak07@gmail.com"
    sender_password = "riya@123"  

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print("Failed to send email:", e)
