import streamlit as st
import google.generativeai as genai
import json
import os

# Sayfa Ayarları
st.set_page_config(page_title="Ilgın Tandoğan - AI Asistanı", page_icon="🤖", layout="wide")

# --- KENAR ÇUBUĞU (Profil Bilgileri) ---
with st.sidebar:
    # Buraya kendi fotoğrafının linkini koyabilirsin veya boş bırakabilirsin
    st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan") 
    st.markdown("### 📍 Ankara, Türkiye")
    st.markdown("📧 ilgintandogan@gmail.com")
    st.markdown("[LinkedIn](http://www.linkedin.com/in/ilgintandogan) | [GitHub](https://github.com/ilgintandogan)")
    
    st.success("🟢 AI Model: Gemini 1.5 Flash (Aktif)")
    
    # API Key Kontrolü
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        st.error("API Key bulunamadı! Lütfen Secrets ayarlarını kontrol et.")
        st.stop()

# --- ANA EKRAN ---
st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")
st.markdown("""
Ben, Ilgın'ın **CV verileri, proje deneyimleri ve kişisel özellikleriyle** eğitilmiş bir yapay zekayım.
Aşağıdaki hazır sorulara tıklayabilir veya aklınızdakini direkt sorabilirsiniz.
""")

st.markdown("---")

# JSON Verisini Yükle
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

try:
    cv_data = load_data()
except FileNotFoundError:
    st.error("data.json dosyası bulunamadı! GitHub'a yüklediğinden emin ol.")
    st.stop()

# --- HAZIR SORU BUTONLARI (2 Satır Halinde) ---
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

prompt_input = None

# 1. Satır Butonları
with col1:
    if st.button("🍊 Portakal Tech Deneyimi", help="Stajda neler yaptı?"):
        prompt_input = "Portakal Technology stajında hangi teknolojileri kullandı, şifresiz deployment gibi spesifik neler yaptı detaylı anlat."

with col2:
    if st.button("🧠 Karakteri & Soft Skills", help="Nasıl bir çalışma arkadaşıdır?"):
        prompt_input = "Ilgın'ın karakteri, stres yönetimi ve çalışma disiplini nasıldır? Sporcu geçmişinin buna etkisi nedir?"

with col3:
    if st.button("🎓 Eğitmenlik & Liderlik", help="Özel ders ve mentörlük deneyimi"):
        prompt_input = "Ilgın'ın özel ders verme (tutor) deneyimi ve Gunkoy projesindeki liderlik/fedakarlık örneklerinden bahset."

# 2. Satır Butonları
with col4:
    if st.button("🛠 Teknik Yetkinlikler", help="Hangi araçları biliyor?"):
        prompt_input = "Ilgın'ın bildiği programlama dilleri, DevOps araçları ve Cloud teknolojileri nelerdir?"

with col5:
    if st.button("🚀 Kendini Nasıl Geliştiriyor?", help="Sertifikalar ve Öğrenme"):
        prompt_input = "Ilgın kendini geliştirmek için neler yapıyor? Aldığı sertifikalar, katıldığı eğitimler ve hobileri neler?"

with col6:
    if st.button("❤️ Sosyal Sorumluluk", help="Gunkoy Projesi"):
        prompt_input = "Gunkoy projesinde köy okulları için neler yaptı? Gece okulda kalıp boya yapması gibi detayları anlat."


# Kullanıcıdan Özel Soru Alma Alanı
st.markdown("---")
user_question = st.chat_input("Veya buraya kendi sorunuzu yazın...")

if user_question:
    prompt_input = user_question

# --- AI CEVAP MEKANİZMASI ---
if prompt_input:
    # Model Kurulumu (En stabil ve ücretsiz model)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Sistem Mesajı (Prompt Engineering) - Detayları kullanması için zorluyoruz
    system_prompt = f"""
    Sen Ilgın Tandoğan'ı temsil eden profesyonel, samimi ve zeki bir AI asistanısın.
    Amacın, işverenlere Ilgın'ın hem teknik becerilerini hem de karakterini en iyi şekilde anlatmak.
    
    Aşağıdaki JSON verisini KESİNLİKLE temel al.
    Özellikle şu detayları vurgula:
    - Portakal Technology'deki "şifresiz deployment" ve "multi-node" çalışmaları.
    - Gunkoy projesindeki "duvar boyama", "gece okulda kalma" gibi fedakarlık detayları.
    - Özel ders verirken geliştirdiği "Adaptive Teaching" yeteneği.
    
    Cevapların akıcı, motive edici ve Türkçe olsun. Ilgın adına konuşabilirsin ("Ben..." diyerek) veya üçüncü şahıs ("Ilgın...") kullanabilirsin.
    
    CV VERİSİ:
    {json.dumps(cv_data, ensure_ascii=False)}
    
    SORU: {prompt_input}
    """

    with st.chat_message("assistant"):
        with st.spinner("Ilgın'ın hafızası taranıyor..."):
            try:
                response = model.generate_content(system_prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
