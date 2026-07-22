import logging
import time

from graph_client import GraphClient
from email_service import build_reply

logging.basicConfig(

    filename="logs/assistant.log",

    level=logging.INFO

)

graph = GraphClient()

processed = set()

while True:

    try:

        response = graph.get_messages()

        if "value" in response:

            for mail in response["value"]:

                mail_id = mail["id"]

                sender = mail["from"]["emailAddress"]["address"]

                if mail_id not in processed:

                    graph.send_mail(build_reply(sender))

                    processed.add(mail_id)

                    logging.info(f"Auto replied to {sender}")

    except Exception as e:

        logging.error(e)

    time.sleep(30)
