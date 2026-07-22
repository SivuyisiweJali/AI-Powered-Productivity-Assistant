AUTO_REPLY = """
Good day Customer,
Thank you for contacting Smart Solution.
Please ensure the email contains your full name,
ID number and cellphone number.
An agent will respond within 24 hours.
Best regards,
Smart Solutions
"""

def build_reply(receiver):
    return {
        "message": {
            "subject": "Automatic Response",
            "body": {
                "contentType": "Text",
                "content": AUTO_REPLY
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": receiver
                    }
                }
            ]
        }
    }
