import streamlit as st
import google.generativeai as genai
import json

# --- Streamlit Sayfa Ayarları ---
st.set_page_config(
    page_title="Ilgın Tandoğan - Dijital İkiz",
    page_icon="🤖",
    layout="wide"
)

# --- Session State ---
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

# --- Sidebar ---
with st.sidebar:
    try:
        st.image("ilgin.jpg", caption="Ilgın Tandoğan", width=150)
    except:
        st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan")

    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](https://linkedin.com/in/ilgintandogan)")
    st.write("[GitHub](https://github.com/ilgintandogan)")

    # API key alma (Streamlit Secrets veya Manuel)
    api_key = st.secrets.get("GEMINI_API_KEY", None) or st.text_input("Google Gemini API Key", type="password")

# --- Ana Başlık ---
st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")

st.markdown("""
Ben, Ilgın'ın **CV verileri, proje deneyimleri ve kişisel özellikleriyle** eğitilmiş bir yapay zekayım.
Ilgın'ın teknik yetkinliklerinin yanı sıra **kariyer hedefleri, proje detayları ve çalışma disiplini** hakkında da bana soru sorabilirsiniz.
""")
st.markdown("---")

# --- JSON Veri Yükleme ---
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

cv_data = load_data()

# --- Manuel Chat Girişi ---
user_question = st.chat_input("Bir soru yazın...")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.get("prompt_input", None)

# --- AI Cevaplama ---
if prompt_input and api_key:

    genai.configure(api_key=api_key)

    # ✔ DOĞRU MODEL → Yeni SDK ile çalışır
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Sisteme gönderilecek içerik
    system_prompt = f"""
    Ilgın Tandoğan'ın CV verileri:
    {json.dumps(cv_data, ensure_ascii=False, indent=2)}

    Kullanıcının sorusu: {prompt_input}

    Lütfen profesyonel, samimi ve akıcı bir şekilde cevap ver.
    """

    try:
        response = model.generate_content(system_prompt)
        answer = response.text

        st.markdown(f"### Soru: {prompt_input}")
        st.write(answer)

        # Input reset
        st.session_state.prompt_input = None

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
