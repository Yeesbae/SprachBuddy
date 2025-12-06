"""
Helper script to find the message_thread_id of a specific channel/topic in your Telegram group.

To use this:
1. Temporarily enable logging in webhook.py to print all message data
2. Send a message to the specific channel/topic you want to monitor
3. Check the logs to find the message_thread_id
4. Set that ID as ALLOWED_TOPIC_ID environment variable
"""

import json
import logging

logger = logging.getLogger(__name__)

def print_message_info(update):
    """
    Prints useful information about a message including topic/channel ID.
    Call this from your webhook to debug.
    """
    message = None
    message_type = None
    
    if "message" in update:
        message = update["message"]
        message_type = "message"
    elif "channel_post" in update:
        message = update["channel_post"]
        message_type = "channel_post"
    
    if message:
        info = {
            "type": message_type,
            "chat_id": message.get("chat", {}).get("id"),
            "chat_title": message.get("chat", {}).get("title"),
            "chat_type": message.get("chat", {}).get("type"),
            "message_id": message.get("message_id"),
            "message_thread_id": message.get("message_thread_id"),  # This is the topic ID!
            "text": message.get("text", "")[:50],  # First 50 chars
            "from_user": message.get("from", {}).get("username") if message.get("from") else None,
        }
        
        separator = "=" * 50
        logger.info(f"\n{separator}\nMESSAGE INFO:\n{json.dumps(info, indent=2)}\n{separator}")
        print(f"\n{separator}\nMESSAGE INFO:\n{json.dumps(info, indent=2)}\n{separator}")
        
        return info
    return None
