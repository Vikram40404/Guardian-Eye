import os
import requests

def send_telegram_alert(
    suspect_img_path,
    full_img_path,
    suspect_labels,
    timestamp,
    camera_location
):
    try:
        bot_token = "8460664302:AAGweGNRjCRThHdThhGdbukRknsAr3gFEOc"
        chat_id = "5533489956"

        lat = camera_location["latitude"]
        lon = camera_location["longitude"]
        address = camera_location["address"]
        google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        label_str = ", ".join(suspect_labels)

        caption = f"""<b>⚠️ Suspect Detected!</b>\n
<b>🕒 Time:</b> {timestamp}\n
<b>🎯 Items:</b> {label_str}\n
<b>📍 Address:</b> {address}\n
<b>🌐 GPS:</b> <a href="{google_maps_link}">{lat}, {lon}</a>
"""

        if os.path.exists(suspect_img_path):
            with open(suspect_img_path, 'rb') as photo:
                response = requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendPhoto",
                    data={
                        'chat_id': chat_id,
                        'caption': caption,
                        'parse_mode': 'HTML'
                    },
                    files={'photo': photo}
                )
                if response.status_code == 200:
                    print("[✔] Telegram alert (suspect image) sent!")
                else:
                    print(f"[✖] Telegram suspect image failed: {response.text}")

        if os.path.exists(full_img_path):
            with open(full_img_path, 'rb') as full_img:
                full_caption = "📷 Full Frame View of Scene"
                response2 = requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendPhoto",
                    data={
                        'chat_id': chat_id,
                        'caption': full_caption,
                        'parse_mode': 'HTML'
                    },
                    files={'photo': full_img}
                )
                if response2.status_code == 200:
                    print("[✔] Telegram alert (full image) sent!")
                else:
                    print(f"[✖] Telegram full image failed: {response2.text}")

    except Exception as e:
        print(f"[✖] Telegram alert error: {e}")

