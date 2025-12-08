import streamlit as st
import json

from google.ai.generativelanguage import GenerativeServiceClient
from google.ai.generativelanguage import Content
from google.api_core.client_options import ClientOptions

st.set_page_config(page_title="Ilgın Tandoğan - Dijital İkiz", page_icon="🤖")

if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

with st.sidebar:
    try:
        st.image("ilgin.jpg", width=150)
    except:
        st.image("https://via.placeholder.com/150")

    st.write("📧 ilgintandogan@gmail.com")

    api_key = st.secrets.get("GEMINI_API_KEY", None) or st.text_input("API Key", type="password")

st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")

def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

cv_data = load_data()

user_question = st.chat_input("Bir soru yazın...")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.prompt_input

if prompt_input and api_key:

    client = GenerativeServiceClient(
        client_options=ClientOptions(
            api_key=api_key,
            api_endpoint="generativelanguage.googleapis.com"
        )
    )

    system_prompt = f"""
    Ilgın Tandoğan'ın CV verileri:
    {json.dumps(cv_data, ensure_ascii=False, indent=2)}

    Soru: {prompt_input}
    """

    try:
        response = client.generate_content(
            model="models/gemini-1.5-flash-001",
            contents=[Content(parts=[{"text": system_prompt}])]
        )

        answer = response.candidates[0].content.parts[0].text
        st.write(answer)

        st.session_state.prompt_input = None

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
