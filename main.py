import time
import random
import requests
import threading
import os
from flask import Flask

# Pulls the Webhook URL securely from Render's Environment Variables
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
ROLE_ID = "1566214495490277487"

# Regions matching your setup
REGIONS = [
    {"name": "EU Central", "color": 0x3498DB},
    {"name": "EU West", "color": 0x2ECC71},
    {"name": "NA East", "color": 0xE67E22},
    {"name": "NA West", "color": 0xF1C40F},
    {"name": "Asia", "color": 0x9B59B6},
    {"name": "Oceania", "color": 0xE74C3C}
]

# Security Shield Logo URL
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/565/565547.png"

# --- FLASK KEEP-ALIVE SERVER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Region Maintenance System is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def send_webhook(embed, content=""):
    if not WEBHOOK_URL:
        print("[ERROR] WEBHOOK_URL environment variable is not set!")
        return
    payload = {
        "content": content,
        "embeds": [embed]
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("[SUCCESS] Webhook sent successfully.")
        else:
            print(f"[ERROR] Failed to send webhook: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"[EXCEPTION] {e}")

def alert_worker():
    print("Region Maintenance Alert Worker Started...")
    while True:
        # 1. Random wait between 2 to 7 minutes (120 to 420 seconds)
        wait_time = random.randint(120, 420)
        print(f"Waiting {wait_time // 60} minutes and {wait_time % 60} seconds before next maintenance alert...")
        time.sleep(wait_time)
        
        # Pick a random region
        region = random.choice(REGIONS)
        
        # 2. Send MAINTENANCE STARTED Alert Embed
        maint_embed = {
            "title": "🛠️ Scheduled Region Maintenance",
            "description": f"**Region:** `{region['name']}`\nStatus: **MAINTENANCE IN PROGRESS**\n\nRoutine infrastructure updates and security maintenance have been initiated for this zone.",
            "color": 0xF1C40F, # Yellow/Gold
            "thumbnail": {"url": LOGO_URL},
            "footer": {"text": "Infrastructure Operations • Automated Alert"}
        }
        send_webhook(maint_embed, content=f"<@&{ROLE_ID}>")
        
        # 3. Random wait between 4 to 25 minutes (240 to 1500 seconds) for LIFTED status
        lift_wait = random.randint(240, 1500)
        print(f"Maintenance active for {region['name']}. Waiting {lift_wait // 60} minutes for maintenance to be lifted...")
        time.sleep(lift_wait)
        
        # 4. Send MAINTENANCE LIFTED Alert Embed
        lifted_embed = {
            "title": "🟢 Maintenance Lifted",
            "description": f"**Region:** `{region['name']}`\nStatus: **ONLINE / NORMAL**\n\nInfrastructure maintenance for this region has been successfully completed and normal operations have resumed.",
            "color": 0x2ECC71, # Green
            "thumbnail": {"url": LOGO_URL},
            "footer": {"text": "Infrastructure Operations • Automated Alert"}
        }
        send_webhook(lifted_embed, content=f"<@&{ROLE_ID}>")

if __name__ == "__main__":
    t = threading.Thread(target=alert_worker)
    t.daemon = True
    t.start()
    run_flask()
