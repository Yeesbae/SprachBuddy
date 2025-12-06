import os

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Channel/Topic filtering
# Set this to the message_thread_id of the specific channel/topic you want to listen to
# Leave as None to listen to all messages
ALLOWED_TOPIC_ID = os.getenv("ALLOWED_TOPIC_ID", None)

# If you need to allow multiple topics, you can use a comma-separated list
# Example: "123,456,789"
ALLOWED_TOPIC_IDS = [49]
if ALLOWED_TOPIC_ID:
    ALLOWED_TOPIC_IDS = [int(tid.strip()) for tid in ALLOWED_TOPIC_ID.split(",") if tid.strip()]
