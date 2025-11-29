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
    st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan")
    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](http://www.linkedin.com/in/ilgintandogan) | [GitHub](https://github.com/ilgintandogan)")
    
    st.success("🟢 Model: Gemini 2.0 Flash")

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
# İK'nın merak edeceği 3 ana kategori: Deneyim, Kişilik, Hedefler

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
    if st.button("📚 Okul Projeleri", help="Bilkent'teki projeler"):
        st.session_state.prompt_input = "Ilgın'ın okulda geliştirdiği Veritabanı ve Mobil Uygulama projelerinden bahset. Hangi teknolojileri kullandı?"

# 2. Satır: Soft Skills & Karakter
with col4:
    if st.button("🧠 Karakter & Soft Skills", help="Nasıl biridir?"):
        st.session_state.prompt_input = "Ilgın'ın karakteri, stres yönetimi ve çalışma disiplini nasıldır? Sporcu geçmişinin iş hayatına etkisi nedir?"

with col5:
    if st.button("🎓 Eğitmenlik & Liderlik", help="Mentörlük deneyimi"):
        st.session_state.prompt_input = "Ilgın'ın özel ders verme (Adaptive Teaching) yeteneği ve öğrencilere yaklaşımı nasıldır?"

with col6:
    if st.button("❤️ Sosyal Sorumluluk", help="Gunkoy Projesi"):
        st.session_state.prompt_input = "Gunkoy projesinde köy okulları için neler yaptı? Gece okulda kalıp boya yapması ve fiziksel katkıları gibi detayları anlat."

# 3. Satır: Vizyon & Problem Çözme
with col7:
    if st.button("🎯 Neden DevOps?", help="Kariyer Hedefi"):
        st.session_state.prompt_input = "Ilgın neden DevOps alanını seçti? Kariyer hedefi nedir ve neden bu alanda başarılı olacağını düşünüyor?"

with col8:
    if st.button("💡 Bir Zorluk & Çözümü", help="Problem çözme yeteneği"):
        st.session_state.prompt_input = "Ilgın'ın teknik bir zorlukla karşılaştığı (örneğin Portakal stajındaki hata) ve bunu nasıl çözdüğüyle ilgili bir anısını anlat."

with col9:
    if st.button("🚀 Kendini Nasıl Geliştiriyor?", help="Sertifikalar ve Hobiler"):
        st.session_state.prompt_input = "Ilgın kendini güncel tutmak için neler yapıyor? Yeni stajı, sertifikaları ve hobileri neler?"


# Chat input (Manuel soru sorma)
user_question = st.chat_input("Veya buraya kendi sorunuzu yazın...")
if user_question:
    st.session_state.prompt_input = user_question

# Prompt'u değişkene alalım
prompt_input = st.session_state.get("prompt_input", None)

# ---- AI CEVAP MEKANİZMASI ----
if prompt_input and api_key:
    client = genai.Client(api_key=api_key)
    MODEL_NAME = "gemini-2.0-flash" 

    # System Prompt: AI'a yeni eklediğimiz alanları da kullanmasını söylüyoruz
    system_prompt = f"""
    Sen Ilgın Tandoğan'ı temsil eden profesyonel, samimi ve zeki bir AI asistanısın.
    Amacın, işverenlere Ilgın'ın hem teknik becerilerini hem de karakterini en iyi şekilde satmak.
    
    Aşağıdaki JSON verisini KESİNLİKLE temel al.
    Cevap verirken şu detayları vurgulamaya özen göster:
    - Teknik konularda: Portakal'daki deployment detayları, okul projeleri ve araç bilgisi.
    - Karakter konularında: Sporcu disiplini, fedakarlık (Günkoy), öğretme yeteneği.
    - Vizyon konularında: Neden DevOps istediği ve problem çözme yaklaşımı.
    
    Cevapların akıcı, motive edici ve Türkçe olsun.
    
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
