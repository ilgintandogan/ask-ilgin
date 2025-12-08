import streamlit as st
import google.generativeai as genai
import json

# --- Streamlit Ayarları ---
st.set_page_config(page_title="Ilgın Tandoğan - Dijital İkiz", page_icon="🤖", layout="wide")

if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

# --- Sidebar ---
with st.sidebar:
    st.image("ilgin.jpg", width=150)
    st.write("📧 ilgintandogan@gmail.com")

    api_key = st.secrets.get("GEMINI_API_KEY") or st.text_input("Gemini API Key", type="password")

st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")
st.markdown("---")

# --- JSON CV verisi ---
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

cv_data = load_data()

# --- Kullanıcı input ---
q = st.chat_input("Bir soru yaz...")

# --- AI Cevap Motoru ---
if q and api_key:
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    full_prompt = f"""
    Sen Ilgın Tandoğan'ı temsil eden profesyonel ve sempatik bir yapay zekâsın.

    Aşağıda Ilgın'ın CV verileri yer alıyor:
    {json.dumps(cv_data, ensure_ascii=False)}

    Soru: {q}
    """

    try:
        response = model.generate_content(full_prompt)
        st.write(response.text)

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
