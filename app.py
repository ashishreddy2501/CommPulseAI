import streamlit as st
from google import genai
from google.genai import types

# --- PAGE CONFIG ---
st.set_page_config(page_title="CommPulse AI", page_icon="💬")

# --- AUTHENTICATION ---
# Streamlit uses st.secrets to keep your API key hidden and safe
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Please set the GOOGLE_API_KEY in your Streamlit Secrets.")
    st.stop()

# Initialize the Gemini Client
client = genai.Client(api_key=API_KEY)

# --- LOGIC ---
def analyze_health(text_log):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Analyze communication health:\n\n{text_log}",
            config=types.GenerateContentConfig(
                system_instruction="Categorize as FLOWING, STALLED, or ESCALATE. Provide a short recommendation.",
                temperature=0.1
            )
        )
        return response.text
    except Exception as e:
        return f"🚨 Error: {e}"

# --- USER INTERFACE ---
st.title("AIRA Test")
st.subheader("Professional Communication Health Analyzer")

with st.expander("How to use"):
    st.write("Paste a chat log or email thread below to see if the conversation is healthy or needs intervention.")

# User Input area
user_input = st.text_area("Paste Conversation Log:", placeholder="User A: Where is the report? 
                            User B: Still waiting on HR. User A: It was due yesterday.", height=200)

if st.button("Analyze Health"):
    if user_input.strip():
        with st.spinner("Analyzing with Gemini..."):
            result = analyze_health(user_input)
            
            # Use columns or cards to display result cleanly
            st.divider()
            st.markdown("### Analysis Result")
            st.info(result)
    else:
        st.warning("Please enter some text to analyze.")

# Footer
st.caption("Powered by Gemini 2.5 Flash | 2026")
