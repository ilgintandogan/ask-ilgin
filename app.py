import streamlit as st
from google import genai
import json

# Sayfa Ayarları
st.set_page_config(page_title="Ilgın Tandoğan - Dijital İkiz", page_icon="🤖", layout="wide")

# ---- SESSION STATE INIT ----
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

# --- SIDEBAR (SOL MENÜ) ---
with st.sidebar:
    
    try:
        st.image("ilgin.jpg", caption="Ilgın Tandoğan", width=150)
    except:
        st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan")

    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](http://www.linkedin.com/in/ilgintandogan) | [GitHub](https://github.com/ilgintandogan)")
    
    # API Key alma
    api_key = st.secrets.get("GEMINI_API_KEY", None) or st.text_input("Google Gemini API Key", type="password")

# --- ANA EKRAN ---
st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")

st.markdown("""
Ben, Ilgın'ın **CV verileri, proje deneyimleri ve kişisel özellikleriyle** eğitilmiş bir yapay zekayım.
Ilgın'ın teknik yetkinliklerinin yanı sıra **kariyer hedefleri, proje detayları ve çalışma disiplini** hakkında da bana soru sorabilirsiniz.
""")
st.markdown("---")

# JSON Verisini Yükle
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

try:
    cv_data = load_data()
except FileNotFoundError:
    st.error("data.json dosyası bulunamadı! Lütfen GitHub'a yüklediğinden emin ol.")
    st.stop()

# --- ÖZELLEŞTİRİLMİŞ BUTONLAR (3x3 Düzen) ---
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)

# 1. Satır
with col1:
    if st.button("🍊 Portakal Tech Deneyimi"):
        st.session_state.prompt_input = "Portakal Technology stajında hangi teknolojileri kullandı?"

with col2:
    if st.button("🛠 Teknik Yetkinlikler"):
        st.session_state.prompt_input = "Ilgın'ın bildiği programlama dilleri ve DevOps teknolojileri nelerdir?"

with col3:
    if st.button("📚 Projeler"):
        st.session_state.prompt_input = "EduGraph, WastlessWorld ve Android projelerini detaylı açıkla."

# 2. Satır
with col4:
    if st.button("🧠 Soft Skills"):
        st.session_state.prompt_input = "Ilgın'ın karakteri ve çalışma disiplini nasıldır?"

with col5:
    if st.button("🎓 Eğitmenlik"):
        st.session_state.prompt_input = "Ilgın'ın özel ders verme yaklaşımı nasıldır?"

with col6:
    if st.button("❤️ Sosyal Sorumluluk"):
        st.session_state.prompt_input = "Gunkoy projesinde neler yaptı?"

# 3. Satır
with col7:
    if st.button("🎯 Neden DevOps?"):
        st.session_state.prompt_input = "Ilgın neden DevOps alanını seçmiştir?"

with col8:
    if st.button("💡 Zorluk & Çözüm"):
        st.session_state.prompt_input = "Ilgın'ın çözdüğü teknik bir sorunu anlat."

with col9:
    if st.button("🚀 Kendini Geliştiriyor"):
        st.session_state.prompt_input = "Ilgın kendini geliştirmek için neler yapıyor?"

# Manuel soru
user_question = st.chat_input("Veya buraya kendi sorunuzu yazın...")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.get("prompt_input", None)

# ---- AI CEVAP MEKANİZMASI ----
if prompt_input and api_key:

    client = genai.Client(api_key=api_key)

    # 🔥 Streamlit Cloud'un şu an desteklediği model
    MODEL_NAME = "gemini-1.5-flash"

    system_prompt = f"""
    Sen Ilgın Tandoğan'ın dijital ikizisin.
    Aşağıdaki CV verilerini temel alarak işverenlere profesyonel ve akıcı cevaplar ver.

    CV VERİSİ:
    {json.dumps(cv_data, ensure_ascii=False)}

    SORU:
    {prompt_input}
    """

    with st.spinner("Ilgın'ın hafızası taranıyor..."):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=system_prompt
            )

            # Yanıt okuma
            answer = getattr(response, "text", None)
            if not answer:
                try:
                    answer = response.candidates[0].content.parts[0].text
                except Exception:
                    answer = str(response)

            st.markdown(f"**Soru:** {prompt_input}")
            st.markdown("---")
            st.markdown(answer)

            st.session_state.prompt_input = None

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
