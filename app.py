import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="Ilgın Tandoğan - Dijital İkiz", page_icon="🤖", layout="wide")

if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

with st.sidebar:
    try:
        st.image("ilgin.jpg", caption="Ilgın Tandoğan", width=150)
    except:
        st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan")

    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](http://www.linkedin.com/in/ilgintandogan)")
    
    api_key = st.secrets.get("GEMINI_API_KEY", None) or st.text_input("Google Gemini API Key", type="password")

st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")

def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

cv_data = load_data()

user_question = st.chat_input("Bir soru yazın...")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.get("prompt_input", None)

if prompt_input and api_key:
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = f"""
    Ilgın Tandoğan'ın CV verileri:
    {json.dumps(cv_data, ensure_ascii=False)}

    SORU: {prompt_input}
    """

    try:
        response = model.generate_content(system_prompt)
        answer = response.text

        st.markdown(f"### Soru: {prompt_input}")
        st.markdown(answer)

        st.session_state.prompt_input = None

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
