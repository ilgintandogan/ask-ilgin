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

# 1. Satır: En Önemli Deneyimler
with col1:
    if st.button("🍊 Portakal Tech Deneyimi", help="Staj detayları"):
        st.session_state.prompt_input = "Portakal Technology stajında hangi teknolojileri kullandı? Özellikle 'şifresiz deployment' ve 'multi-node' çalışmalarını detaylı anlat."

with col2:
    if st.button("🛠 Teknik Yetkinlikler", help="Araçlar ve Diller"):
        st.session_state.prompt_input = "Ilgın'ın bildiği programlama dilleri, DevOps araçları (Kubernetes, OpenStack vb.) ve Cloud teknolojileri nelerdir?"

with col3:
    if st.button("📚 Projeler (EduGraph, Web, Mobil)", help="Okul ve Kişisel Projeler"):
        st.session_state.prompt_input = "Ilgın'ın geliştirdiği en önemli proje olan EduGraph (AI YKS Koçu), WastlessWorld (PHP/SQL Web) ve Android Studio mobil uygulama projelerini detaylı anlat."

# 2. Satır: Soft Skills & Karakter
with col4:
    if st.button("🧠 Karakter & Soft Skills", help="Nasıl biridir?"):
        st.session_state.prompt_input = "Ilgın'ın karakteri, çalışma disiplini, stres yönetimi ve spor geçmişinin iş hayatına etkisi nedir?"

with col5:
    if st.button("🎓 Eğitmenlik & Liderlik", help="Mentörlük deneyimi"):
        st.session_state.prompt_input = "Ilgın'ın özel ders verme (Adaptive Learning) yeteneği ve öğrencilere yaklaşımı nasıldır?"

with col6:
    if st.button("❤️ Sosyal Sorumluluk", help="Gunkoy Projesi"):
        st.session_state.prompt_input = "Gunkoy projesinde köy okulları için neler yaptı? Gece okulda kalıp boya yapması ve fiziksel katkıları gibi detayları anlat."

# 3. Satır: Vizyon & Problem Çözme
with col7:
    if st.button("🎯 Neden DevOps?", help="Kariyer Hedefi"):
        st.session_state.prompt_input = "Ilgın neden DevOps alanını seçti? Kariyer hedefi nedir ve neden bu alanda başarılı olacağını düşünüyor?"

with col8:
    if st.button("💡 Bir Zorluk & Çözümü", help="Problem çözme yeteneği"):
        st.session_state.prompt_input = "Ilgın'ın bir teknik sorunla karşılaşıp çözdüğü bir anısını anlat."

with col9:
    if st.button("🚀 Kendini Nasıl Geliştiriyor?", help="Sertifikalar ve Hobiler"):
        st.session_state.prompt_input = "Ilgın kendini güncel tutmak için neler yapıyor? Sertifikaları, hobileri ve yeni staj planları nelerdir?"

# Manuel soru
user_question = st.chat_input("Veya buraya kendi sorunuzu yazın...")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.get("prompt_input", None)

# ---- AI CEVAP MEKANİZMASI ----
if prompt_input and api_key:
    client = genai.Client(api_key=api_key)

    # 🔥 DOĞRU MODEL — free tier çalışır
    MODEL_NAME = "gemini-pro"

    system_prompt = f"""
    Sen Ilgın Tandoğan’ı temsil eden profesyonel, samimi, motive edici ve zeki bir AI asistanısın.
    Amacın, işverenlere Ilgın'ın hem teknik becerilerini hem de karakterini en iyi şekilde aktarmak.
    Aşağıdaki JSON verisini KESİNLİKLE temel al.
    
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

            answer = getattr(response, "text", None)
            if not answer:
                try:
                    answer = response.output[0].content[0].text
                except Exception:
                    answer = str(response)

            st.markdown(f"**Soru:** {prompt_input}")
            st.markdown("---")
            st.markdown(answer)

            st.session_state.prompt_input = None

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
