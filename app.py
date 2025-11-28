import streamlit as st
from google import genai
import json
import os

# Sayfa Ayarları
st.set_page_config(page_title="Ilgın Tandoğan - AI Asistanı", page_icon="🤖")

# --- KENAR ÇUBUĞU (Profil Bilgileri) ---
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan")
    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](http://www.linkedin.com/in/ilgintandogan) | [GitHub](https://github.com/ilgintandogan)")
    
    # API Key alma
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        api_key = st.text_input("Google Gemini API Key", type="password")

# --- ANA EKRAN ---
st.title("Merhaba! Ben Ilgın'ın AI Asistanıyım 👋")
st.write("""
Ben Ilgın'ın CV verileriyle eğitilmiş bir yapay zekayım. 
Bana onun **DevOps tecrübeleri, projeleri, sertifikaları veya eğitimi** hakkında soru sorabilirsiniz.
""")

# JSON verisini yükle
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

try:
    cv_data = load_data()
except FileNotFoundError:
    st.error("data.json dosyası bulunamadı!")
    st.stop()

# Hazır sorular
col1, col2, col3 = st.columns(3)
if col1.button("🎓 Eğitimi nedir?"):
    prompt_input = "Eğitim geçmişinden bahset."
elif col2.button("🛠 Hangi araçları biliyor?"):
    prompt_input = "Teknik yetkinlikleri ve bildiği araçlar neler?"
elif col3.button("💼 DevOps deneyimi var mı?"):
    prompt_input = "DevOps ve Cloud alanındaki deneyimlerinden bahset."
else:
    prompt_input = None

# Kullanıcı Soru
user_question = st.chat_input("Ilgın hakkında ne merak ediyorsunuz?")

if user_question:
    prompt_input = user_question

# --- AI CEVAP MEKANİZMASI ---
if prompt_input and api_key:

    # Google GenAI Client
    client = genai.Client(api_key=api_key)

    # Gemini modeli (Google AI Studio'da en stabil model)
    MODEL_NAME = "gemini-2.0-flash"  # erişimin varsa gemini-2.0-pro da olur

    system_prompt = f"""
    Sen Ilgın Tandoğan'ı temsil eden yardımsever ve profesyonel bir asistanısın.
    Aşağıdaki JSON formatındaki CV verilerini kullanarak sorulara cevap ver.
    Cevapların kısa, net ve profesyonel olsun.
    Eğer CV'de olmayan bir bilgi sorulursa, kibarca bilmediğini söyle ve mail adresine yönlendir.

    CV VERİSİ:
    {json.dumps(cv_data, ensure_ascii=False)}

    SORU: {prompt_input}
    """

    with st.spinner("Ilgın'ın hafızası taranıyor..."):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=system_prompt
            )

            # Gemini response yapısı
            answer = response.text

            st.markdown(f"**Soru:** {prompt_input}")
            st.markdown("---")
            st.markdown(answer)

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

elif prompt_input and not api_key:
    st.warning("Lütfen önce API anahtarını giriniz.")
