import streamlit as st
import google.generativeai as genai
import json
import os

# Sayfa Ayarları
st.set_page_config(page_title="Ilgın Tandoğan - AI Asistanı", page_icon="🤖")

# --- KENAR ÇUBUĞU (Profil Bilgileri) ---
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan") # Buraya kendi foto linkini koyabilirsin
    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](http://www.linkedin.com/in/ilgintandogan) | [GitHub](https://github.com/ilgintandogan)")
    
    # API Key Girişi (Güvenlik için kullanıcıdan istiyoruz veya secrets'tan çekiyoruz)
    # Eğer GitHub'a yükleyeceksen bu key'i kodun içine ASLA yazma.
    # Streamlit Secrets kullanacağız.
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

# JSON Verisini Yükle
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

try:
    cv_data = load_data()
except FileNotFoundError:
    st.error("data.json dosyası bulunamadı!")
    st.stop()

# Hazır Sorular (Butonlar)
col1, col2, col3 = st.columns(3)
if col1.button("🎓 Eğitimi nedir?"):
    prompt_input = "Eğitim geçmişinden bahset."
elif col2.button("🛠 Hangi araçları biliyor?"):
    prompt_input = "Teknik yetkinlikleri ve bildiği araçlar neler?"
elif col3.button("💼 DevOps deneyimi var mı?"):
    prompt_input = "DevOps ve Cloud alanındaki deneyimlerinden bahset."
else:
    prompt_input = None

# Kullanıcıdan Soru Alma
user_question = st.chat_input("Ilgın hakkında ne merak ediyorsunuz?")

if user_question:
    prompt_input = user_question

# --- AI CEVAP MEKANİZMASI ---
if prompt_input and api_key:
    # Model Kurulumu
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Ücretsiz ve hızlı model

    # Sistem Mesajı (Prompt Engineering)
    system_prompt = f"""
    Sen Ilgın Tandoğan'ı temsil eden yardımsever ve profesyonel bir asistanısın.
    Aşağıdaki JSON formatındaki CV verilerini kullanarak sorulara cevap ver.
    Cevapların kısa, net ve birinci tekil şahıs ağzından (Ilgın gibi) veya "Ilgın..." şeklinde üçüncü şahıs olabilir.
    Eğer CV'de olmayan bir bilgi sorulursa, kibarca bilmediğini söyle ve mail adresine yönlendir.
    
    CV VERİSİ:
    {json.dumps(cv_data, ensure_ascii=False)}
    
    SORU: {prompt_input}
    """

    with st.spinner("Ilgın'ın hafızası taranıyor..."):
        try:
            response = model.generate_content(system_prompt)
            st.markdown(f"**Soru:** {prompt_input}")
            st.markdown("---")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

elif prompt_input and not api_key:
    st.warning("Lütfen önce API anahtarını giriniz.")
