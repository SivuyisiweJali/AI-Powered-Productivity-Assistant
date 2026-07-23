import logging
import time
import os
import signal
import sys
from graph_client import GraphClient
from email_service import build_reply

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/assistant.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

graph = GraphClient()
processed = set()
running = True

def signal_handler(signum, frame):
    """Handle graceful shutdown on SIGTERM/SIGINT"""
    global running
    logging.info("Shutdown signal received. Stopping assistant...")
    running = False
    sys.exit(0)

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

while running:
    try:
        response = graph.get_messages()
        if "value" in response:
            for mail in response["value"]:
                mail_id = mail.get("id")
                sender = mail.get("from", {}).get("emailAddress", {}).get("address")
                
                # Validate required fields
                if not mail_id or not sender:
                    logging.warning(f"Skipping mail with invalid structure: {mail}")
                    continue
                
                if mail_id not in processed:
                    try:
                        graph.send_mail(build_reply(sender))
                        processed.add(mail_id)
                        logging.info(f"Auto replied to {sender}")
                    except Exception as e:
                        logging.error(f"Failed to send reply to {sender}: {str(e)}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")

    time.sleep(30)
