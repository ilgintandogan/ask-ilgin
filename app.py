import streamlit as st
from openai import OpenAI
import json

st.set_page_config(page_title="Ilgın Tandoğan - Dijital İkiz", page_icon="🤖", layout="wide")

if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

with st.sidebar:
    st.image("ilgin.jpg", width=150)
    st.write("📧 ilgintandogan@gmail.com")

    api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("OpenAI API Key", type="password")

st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")
st.markdown("---")

# Load CV
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

cv_data = load_data()

q = st.chat_input("Bir soru yaz…")
if q:
    st.session_state.prompt_input = q

prompt = st.session_state.prompt_input

if prompt and api_key:

    client = OpenAI(api_key=api_key)

    system_prompt = f"""
    Sen Ilgın Tandoğan'ı temsil eden profesyonel ve sempatik bir yapay zekâsın.

    CV verileri:
    {json.dumps(cv_data, ensure_ascii=False)}

    Soru:
    {prompt}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # Çok hızlı + çok ucuz + çok kaliteli
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content
        st.write(answer)

        st.session_state.prompt_input = None

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
