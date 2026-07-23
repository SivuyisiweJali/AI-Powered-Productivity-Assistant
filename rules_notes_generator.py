from openai import OpenAI
from config import OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)
class MeetingSummarizer:
    def generate_summary(self, transcript):
        prompt = f"""
You are an AI Meeting Assistant.
Rules
1. Maximum 200 words.
2. Use simple English.
3. Prioritize
Financial
Technical
Human Resources
4. Ignore greetings.
5. Produce
Executive Summary
Financial
Technical
Human Resources
Action Items
Transcript
{transcript}
"""
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
