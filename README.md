# AI-Powered-Productivity-Assistant

Problem statement

This dashboard aims to help a company that uses traditional task execution methods such as using paper diaries to plan and write meeting notes, interaction with customers is limited to calls and paper document and write the same emails multiple times. 

Solution overview and Key functions

This dashboard will help a company automate its processes using AI. The company will then be able to use the following tools and features:
- Meeting notes summeriser
  1. Speach to text conversion
  2. Financial key word detection
  3. Technical key words detection
  4. Human resources key words detection
- Smart email generator
  1. Automatic reply
  2. Professional email template
  3. 24 hour response notice 
- AI Chatbox Interface
  1. 24/7 availability
  2. Natural language processing
  3. Instant responses
  4. Personalised responses

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
1. ASK AI CHATBOX
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

DEMO
[Smart Outlook Email Generator Assistant – Test Run Demo]
Time	Screen	Narration
0:00–0:10	GitHub repository home page	"This is the Smart Outlook Email Generator Assistant. It automatically replies to incoming emails using the Microsoft Graph API and Microsoft Outlook."
0:10–0:25	Open the project in Visual Studio Code	"The project is organized into modular files, including the main application, email handler, Graph client, configuration, logging, and automated tests."
0:25–0:40	Show the .env file (mask the secrets)	"The application uses Azure Active Directory credentials stored securely in environment variables rather than hard-coded into the source code."
0:40–0:55	Open a terminal and run python app.py	"The assistant starts successfully and begins monitoring the Outlook inbox every 30 seconds for new unread emails."
0:55–1:20	Send a test email from another Outlook account to sivuyisiwe.jali@capaciti.org.za	"A customer sends a new email requesting assistance. The assistant detects the unread message automatically."
1:20–1:45	Open the sender's mailbox	"Within a few seconds, the customer receives an automatic acknowledgement email."
1:45–2:05	Open the automatic reply	Read the reply aloud: "Good day Customer. Thank you for contacting Smart Solution. Please ensure the email contains your full name, ID number and cellphone number. An agent will respond within 24 hours. Best regards, Smart Solutions."
2:05–2:20	Show the original email marked as read	"The assistant marks the processed email as read, preventing duplicate automatic replies."
2:20–2:35	Open assistant.log	"Each successful reply is recorded in the log file for monitoring, auditing, and troubleshooting."
2:35–2:50	Run pytest in the terminal	"Finally, the automated unit tests verify that the reply template and core functionality behave as expected."
2:50–3:00	Return to the GitHub repository	"This concludes the demonstration. The Smart Outlook Email Generator Assistant improves customer response times, reduces manual work, and provides reliable, secure email automation."

[MEETING NOTES GENERATOR ASSISTANT]

Open a terminal.
Run:
git clone https://github.com/yourusername/AI-Meeting-Notes-Summariser.git
cd AI-Meeting-Notes-Summariser
pip install -r requirements.txt
python app.py

Narration:

"The application is installed from GitHub, dependencies are loaded, and the AI assistant is started."

Scene 3 – Microsoft Teams Meeting (0:40–1:00)

Screen:

Open Microsoft Teams.
Join a meeting.
Click Start Recording (or open a recorded meeting).

Narration:

"The assistant connects to Microsoft Teams and captures the meeting audio for processing."

Scene 4 – Speech-to-Text (1:00–1:20)

Screen:
Display a live transcript similar to:

Manager:
The budget for Project Alpha has been approved.

Developer:
API testing will be completed on Friday.

HR:
Recruitment for two software engineers starts next week.

Narration:

"Speech is automatically converted into text using an AI speech recognition model."

Scene 5 – AI Processing (1:20–1:45)

Screen:

Processing Transcript...

✔ Detecting Financial Keywords
✔ Detecting Technical Keywords
✔ Detecting HR Keywords
✔ Extracting Decisions
✔ Identifying Action Items

Generating Summary...

Narration:

"The AI analyses the transcript, prioritises financial, technical, and HR topics, and extracts decisions and action items."

Scene 6 – Final Summary (1:45–2:20)

Screen:

Meeting Summary

• Budget approved for Project Alpha.
• API testing completes Friday.
• HR recruiting two software engineers.
• Security testing begins Monday.

Action Items

John
- Complete API testing
- Friday

Sarah
- Recruit engineers
- Next Week

David
- Prepare budget report
- Monday

Narration:

"Within seconds, the assistant produces a concise summary, highlights key decisions, and assigns action items with responsible team members and deadlines."

Scene 7 – Save & Email (2:20–2:40)

Screen:

✔ Summary Saved

✔ Email Sent

meeting_summary.pdf

meeting_summary.docx

Narration:

"The summary is saved and automatically shared with meeting participants."

Scene 8 – Closing (2:40–3:00)

Screen:
Return to the GitHub repository showing:

README
Source code
Test cases
Workflow diagram

Narration:

"The AI Meeting Notes Summariser improves productivity by automating meeting documentation, reducing manual effort, and ensuring important discussions, decisions, and action items are accurately captured. Thank you for watching."

[ASK AI CHATBOX]

|  SCENE 1: Local Terminal Launch                                           |
|  ▶ user$ streamlit run app.py                                            |
|  ✔ "Running on http://localhost:8501"                                    |
+--------------------------------------------------------------------------+
                                     │
                                     ▼
+--------------------------------------------------------------------------+

|  SCENE 2: The Core Workspace Interface                                   |
|  💻 Sleek Dark/Light layout labeled "🤖 ASK AI Workspace"                |
|  📎 Sidebar showing active file uploader drop-zone                       |
+--------------------------------------------------------------------------+
                                     │
                                     ▼
+--------------------------------------------------------------------------+

|  SCENE 3: Multimodal Upload Demonstration                                |
|  📁 Drag-and-drop a data file or image into the sidebar                  |
|  ✔ Alert banner displays: "Successfully attached: document.txt"         |
+--------------------------------------------------------------------------+
                                     │
                                     ▼
+--------------------------------------------------------------------------+

|  SCENE 4: Live Scholar Grounding & Query Processing                      |
|  💬 User enters a highly complex, academic query                         |
|  ⏳ Real-time streaming response loads under 2 seconds                    |
+--------------------------------------------------------------------------+


Tools,workflow and presentation: 
[https://capeitinitiative-my.sharepoint.com/:p:/g/personal/sivuyisiwe_jali_capaciti_org_za/IQAyRrkHwucOSo6E5wrMtKNVARbAJvDgVwJNlxSL4HMPEyg](https://capeitinitiative-my.sharepoint.com/:p:/g/personal/sivuyisiwe_jali_capaciti_org_za/IQBnznVl79bbQokm96Xyj0sZAQo-f1bgQ0mO1yLrXDfYhro)


