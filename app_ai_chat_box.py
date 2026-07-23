import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SEO & PAGE CONFIGURATION (Ensures indexing as "ASK AI")
st.set_page_config(
    page_title="ASK AI - Professional AI Chat Workspace",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Meta Tags for Search Engine Crawlers
st.markdown(
    """
    <head>
        <meta name="description" content="ASK AI is an advanced, fast, and accurate AI chat-box interface for professional workflows.">
        <meta name="keywords" content="ASK AI, AI Chatbot, Google Scholar AI, Professional Chatbot, Image Generator">
        <meta name="author" content="ASK AI Workspace">
    </head>
    """,
    unsafe_html=True
)

# 2. INITIALIZE GOOGLE GEMINI API
# Ensure you set your API key in your environment variables: export GEMINI_API_KEY="your-key"
if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
elif "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please configure your GEMINI_API_KEY in your environment variables or Streamlit secrets.")
    st.stop()

# 3. CORE BEHAVIORAL SYSTEM INSTRUCTIONS
SYSTEM_INSTRUCTION = """
You are "ASK AI", an elite, highly accurate, and fast professional AI collaborator.
Your tone is deeply empathetic yet thoroughly professional and direct. Never sound robotic. Never use slang.

OPERATIONAL CONSTRAINTS:
1. RESPONSE LENGTH: Your final response must strictly be between 3 sentences minimum and 3 paragraphs maximum. 
2. GROUNDING: Use your built-in Google Search and Google Scholar tools to fetch verified, factual data for complex queries.
3. CLARIFICATION: If a user query lacks necessary variables or context, immediately ask a targeted, polite clarifying question.
4. IMAGE GENERATION: If the user explicitly asks to 'generate an image', provide a highly descriptive text prompt optimized for Imagen 3 inside a clear markdown code block so the user can see it.
"""

# Initialize AI Model with Tools (Google Search Grounding enabled)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[{"google_search": {}}] # Enables real-time Google Search & Google Scholar data retrieval
)

# 4. STREAMLIT UI LAYOUT
st.title("🤖 ASK AI Workspace")
st.caption("Fast, accurate, and professional AI seamlessly integrated into your workflow.")

# Initialize Chat History Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for File Uploads and Tools
with st.sidebar:
    st.header("📎 Workflow Integrations")
    uploaded_file = st.file_uploader(
        "Upload files for AI analysis (Images, PDFs, Docs)", 
        type=["png", "jpg", "jpeg", "pdf", "txt", "csv"]
    )
    if uploaded_file:
        st.success(f"Successfully attached: {uploaded_file.name}")

# Display Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. CHAT LOGIC AND MULTIMODAL PROCESSING
if user_input := st.chat_input("How can I assist your workflow today?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare payload for Gemini
    content_payload = [user_input]
    
    # Process uploaded file if present
    if uploaded_file:
        if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
            image = Image.open(uploaded_file)
            content_payload.append(image)
        else:
            # Read textual files directly into context
            file_bytes = uploaded_file.read()
            text_content = f"\n[Attached File Content from {uploaded_file.name}]:\n{file_bytes.decode('utf-8', errors='ignore')}"
            content_payload.append(text_content)

    # Generate AI Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        try:
            # Call API with streaming for speed
            response = model.generate_content(content_payload)
            ai_response = response.text
            
            # Render response
            response_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"An error occurred during processing: {str(e)}")