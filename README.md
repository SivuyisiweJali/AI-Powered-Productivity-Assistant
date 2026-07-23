# AI-Powered-Productivity-Assistant

Problem statement

This dashboard aims to help a company that uses traditional task execution methods such as using paper diaries to plan and write meeting notes, interaction with customers is limited to calls and paper document and write the same emails multiple times. 

Solution overview

This dashboard will help a company automate its processes using AI. The company will then be able to use the following core features:
- Meeting notes summeriser
- Smart email generator
- AI Chatbox Interface

The purpuse of the features is to: 
- Save time by automating repetitive tasks
- Reduce human error
- Help with uniformity across the organisation
- Improve productivity

  
Tools used
- ChatGPT
- Github copilot
- Gemini

**Installation guide:**
1. For ASK AI Chatbox
ASK AI - Professional Workflow Chat Interface

ASK AI is an optimized, high-performance web interface designed for seamless enterprise integration. Powered by Google Gemini 2.5 Flash and Streamlit, it bridges the gap between fast AI execution and real-world workspace utility.

---

 Core Features

*   **Global SEO Optimization**: Built-in metadata infrastructure engineered to rank effectively for the search query "ASK AI".
*   **Dual-Engine Grounding**: Live data fetching from Google Search and Google Scholar to eliminate factual hallucinations.
*   **Multimodal Processing**: Native support for text entry, image parsing, and complex text data sheet uploads (CSV, TXT, PDF).
*   **Enforced Output Bounds**: Programmatic guardrails that lock responses to a strict 3-sentence minimum and 3-paragraph maximum.
*   **Clarity-First Persona**: Professional tone that automatically asks targeted clarifying questions if your intent or prompt is vague.

---

## 🛠️ Tech Stack

*   **Frontend**: Streamlit (Python)
*   **AI Engine**: Google Gemini 2.5 Flash API
*   **Grounding Engine**: Google Search & Google Scholar Tooling
*   **Image Handling**: Pillow (PIL)

---

## 🚀 Quick Start Guide

### Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com
cd ASK-AI
```

### 2. Install Dependencies
```bash
pip install streamlit google-generativeai pillow
```

### 3. Configure Your Secrets
You must obtain a free API key from Google AI Studio. Set it in your environment variables to keep it secure:

*   **Linux/macOS**:
    ```bash
    export GEMINI_API_KEY="your_actual_api_key_here"
    ```
*   **Windows (Command Prompt)**:
    ```cmd
    set GEMINI_API_KEY="your_actual_api_key_here"
    ```

### 4. Launch the Workspace
```bash
streamlit run app.py
```

---

## ☁️ Free Cloud Deployment (Streamlit Community Cloud)

1. Push your completed code repository to GitHub.
2. Visit [share.streamlit.io](https://streamlit.io) and log in with your GitHub account.
3. Click **New app**, select your repository, branch, and set the main file to `app.py`.
4. Expand **Advanced settings**, and paste your API key into the **Secrets** box:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
5. Click **Deploy**. Your app will be live and indexable by search engines under "ASK AI".

---

## 📜 License

This project is licensed under the MIT License. Feel free to fork, modify, and distribute it for personal or commercial workflows.

2. For email generator
# Smart Outlook Email Generator Assistant
# Author: Smart Solutions
# Requirements:
# pip install msal requests python-dotenv

import os
import time
import requests
import msal
from dotenv import load_dotenv

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
EMAIL_ADDRESS = "sivuyisiwe.jali@capaciti.org.za"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]
GRAPH_URL = "https://graph.microsoft.com/v1.0"

# -------------------------------
# Auto Reply Message
# -------------------------------
AUTO_REPLY_MESSAGE = """
Good day Customer,

Thank you for contacting Smart Solution.

Please ensure the email contains your full name, ID number and cellphone number.

An agent will respond within 24 hours.

Best regards,

Smart Solutions
"""

# -------------------------------
# Authentication
# -------------------------------
def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=SCOPES)

    if "access_token" not in result:
        raise Exception("Failed to obtain access token.")

    return result["access_token"]

# -------------------------------
# Headers
# -------------------------------
def get_headers():
    return {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

# -------------------------------
# Get Unread Emails
# -------------------------------
def get_unread_emails():
    url = (
        f"{GRAPH_URL}/users/{EMAIL_ADDRESS}"
        "/mailFolders/Inbox/messages"
        "?$filter=isRead eq false"
        "&$top=10"
    )

    response = requests.get(url, headers=get_headers())
    response.raise_for_status()

    return response.json().get("value", [])

# -------------------------------
# Send Auto Reply
# -------------------------------
def send_auto_reply(sender_email, subject):

    payload = {
        "message": {
            "subject": f"Re: {subject}",
            "body": {
                "contentType": "Text",
                "content": AUTO_REPLY_MESSAGE
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": sender_email
                    }
                }
            ]
        },
        "saveToSentItems": True
    }

    response = requests.post(
        f"{GRAPH_URL}/users/{EMAIL_ADDRESS}/sendMail",
        headers=get_headers(),
        json=payload
    )

    response.raise_for_status()

# -------------------------------
# Mark Email As Read
# -------------------------------
def mark_as_read(message_id):

    response = requests.patch(
        f"{GRAPH_URL}/users/{EMAIL_ADDRESS}/messages/{message_id}",
        headers=get_headers(),
        json={"isRead": True}
    )

    response.raise_for_status()

# -------------------------------
# Main Processing Loop
# -------------------------------
def process_emails():

    emails = get_unread_emails()

    for email in emails:

        sender = email["from"]["emailAddress"]["address"]
        subject = email.get("subject", "No Subject")
        message_id = email["id"]

        print(f"Processing email from: {sender}")

        send_auto_reply(sender, subject)
        mark_as_read(message_id)

        print(f"Auto reply sent to: {sender}")

# -------------------------------
# Main Application
# -------------------------------
if __name__ == "__main__":

    print("Smart Outlook Email Generator Assistant Started...")

    while True:
        try:
            process_emails()

        except Exception as error:
            print(f"Error: {error}")

        # Check inbox every 30 seconds
        time.sleep(30)
3. For meeting notes summariser
   +--------------------------------------------------------------------------+
|                  AI MEETING NOTES SUMMARISER - SYSTEM FLOW                |
+--------------------------------------------------------------------------+

                     +----------------------+
                     |   Meeting Starts     |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Capture Audio Input  |
                     | (Microsoft Teams)    |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Speech-to-Text (AI)  |
                     | Convert Audio to Text|
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Clean Transcript     |
                     | Remove Noise/Fillers |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Keyword Detection    |
                     | Finance | Technical  |
                     | Human Resources      |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | AI Summarisation     |
                     | Generate <200 Words  |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Extract Decisions    |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Extract Action Items |
                     | Person | Task | Date |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Generate Final Report|
                     +----------+-----------+
                                |
                 +--------------+--------------+
                 |                             |
                 v                             v
      +----------------------+      +----------------------+
      | Save to Database     |      | Email Summary        |
      | Searchable Archive   |      | Send to Participants |
      +----------------------+      +----------------------+

==========================================================================

INPUT
-----
• Microsoft Teams Meeting
• Live Audio
• Recorded Audio

                │
                ▼

PROCESS
-------
1. Capture meeting audio
2. Convert speech to text
3. Clean transcript
4. Detect Financial keywords
5. Detect Technical keywords
6. Detect HR keywords
7. Generate AI summary
8. Extract key decisions
9. Identify action items
10. Save and distribute summary

                │
                ▼

OUTPUT
------
✓ Meeting Summary
✓ Key Decisions
✓ Action Items
✓ Responsible Persons
✓ Deadlines
✓ Financial Highlights
✓ Technical Highlights
✓ HR Highlights
✓ Searchable Meeting Record





Tools,workflow and presentation: 
[https://capeitinitiative-my.sharepoint.com/:p:/g/personal/sivuyisiwe_jali_capaciti_org_za/IQAyRrkHwucOSo6E5wrMtKNVARbAJvDgVwJNlxSL4HMPEyg](https://capeitinitiative-my.sharepoint.com/:p:/g/personal/sivuyisiwe_jali_capaciti_org_za/IQBnznVl79bbQokm96Xyj0sZAQo-f1bgQ0mO1yLrXDfYhro)


