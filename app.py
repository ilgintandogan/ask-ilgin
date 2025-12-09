import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="Ilgın Tandoğan - Dijital İkiz", page_icon="🤖", layout="wide")

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
    st.write("[LinkedIn](http://www.linkedin.com/in/ilgintandogan) | [GitHub](https://github.com/ilgintandogan)")

    api_key = st.secrets.get("GEMINI_API_KEY", None) or st.text_input("Google Gemini API Key", type="password")

# --- Main screen ---
st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")

st.markdown("""
Ben, Ilgın'ın **CV verileri, proje deneyimleri ve kişisel özellikleriyle** eğitilmiş bir yapay zekayım.
Ilgın'ın teknik yetkinlikleri, kariyer hedefleri ve projeleri hakkında bana soru sorabilirsiniz.
""")
st.markdown("---")

# JSON yükleme
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

try:
    cv_data = load_data()
except FileNotFoundError:
    st.error("data.json bulunamadı! GitHub'a yüklediğinden emin ol.")
    st.stop()

# Soru input
user_question = st.chat_input("Bir soru yaz…")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.get("prompt_input", None)

# ---- AI ----
if prompt_input and api_key:
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("models/gemini-1.5-flash-lite")

    system_prompt = f"""
    Sen Ilgın Tandoğan'ı temsil eden profesyonel ve samimi bir yapay zekasın.
    Aşağıdaki CV verisini temel alarak cevap ver:

    {json.dumps(cv_data, ensure_ascii=False)}

    Kullanıcı sorusu:
    {prompt_input}
    """

    with st.spinner("Ilgın'ın hafızası taranıyor…"):
        try:
            response = model.generate_content(system_prompt)
            st.markdown(f"**Soru:** {prompt_input}")
            st.markdown("---")
            st.markdown(response.text)

            st.session_state.prompt_input = None

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
