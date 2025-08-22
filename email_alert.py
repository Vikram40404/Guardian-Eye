import smtplib
import ssl
from email.message import EmailMessage
import os

def send_email_alert(
    suspect_img_path,
    full_img_path,
    suspect_labels,
    timestamp,
    camera_location,
    csv_path="detection.csv"
):
    try:
        print("[EMAIL] Preparing email...")

        if not os.path.exists(suspect_img_path):
            raise FileNotFoundError(f"Suspect image path missing: {suspect_img_path}")
        if not os.path.exists(full_img_path):
            raise FileNotFoundError(f"Full frame image path missing: {full_img_path}")

        sender = "vikrambudaniya420@gmail.com"
        receiver = "vikram005500@gmail.com"
        app_password = "alkaeiubldlkxizg"
        subject = "🔴 Suspect Object Detected!"

        gps_coords = f"{camera_location['latitude']},{camera_location['longitude']}"
        address = camera_location["address"]
        google_maps_link = f"https://maps.google.com/?q={gps_coords}"
        suspect_items = ", ".join(suspect_labels)

        body = f"""\
⚠️ A suspect object was detected on surveillance.

📅 Date & Time: {timestamp}
🕵️ Suspect Items: {suspect_items}

📍 Camera Location:
{address}
🌐 Map: {google_maps_link}

📎 Attached: Suspect Image, Full Frame Image, Log File
"""

        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.set_content(body)

        with open(suspect_img_path, "rb") as img:
            msg.add_attachment(img.read(), maintype="image", subtype="jpeg", filename="suspect.jpg")

        with open(full_img_path, "rb") as img:
            msg.add_attachment(img.read(), maintype="image", subtype="jpeg", filename="full_frame.jpg")

        if csv_path and os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename=os.path.basename(csv_path))

        print("[EMAIL] Connecting to SMTP server...")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender, app_password)
            smtp.send_message(msg)

        print("[✔] Email alert sent successfully!")

    except Exception as e:
        print(f"[✖] Failed to send email alert: {e}")

