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
Ilgın'ın teknik yetkinliklerinin yanı sıra **karakteri, çalışma disiplini ve sosyal yönleri** hakkında da bana soru sorabilirsiniz.
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

# --- ÖZELLEŞTİRİLMİŞ BUTONLAR (3x2 Düzen) ---
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

# 1. Satır
with col1:
    if st.button("🍊 Portakal Tech Deneyimi", help="Stajda neler yaptı?"):
        st.session_state.prompt_input = "Portakal Technology stajında hangi teknolojileri kullandı? Özellikle 'şifresiz deployment' ve 'multi-node' çalışmalarını detaylı anlat."

with col2:
    if st.button("🧠 Karakter & Soft Skills", help="Nasıl biridir?"):
        st.session_state.prompt_input = "Ilgın'ın karakteri, stres yönetimi ve çalışma disiplini nasıldır? Sporcu geçmişinin iş hayatına etkisi nedir?"

with col3:
    if st.button("🎓 Eğitmenlik & Liderlik", help="Özel ders ve mentörlük"):
        st.session_state.prompt_input = "Ilgın'ın özel ders verme (Adaptive Teaching) yeteneği ve Gunkoy projesindeki liderlik/fedakarlık örneklerinden bahset."

# 2. Satır
with col4:
    if st.button("🛠 Teknik Yetkinlikler", help="Hangi araçları biliyor?"):
        st.session_state.prompt_input = "Ilgın'ın bildiği programlama dilleri, DevOps araçları (Kubernetes, OpenStack vb.) ve Cloud teknolojileri nelerdir?"

with col5:
    if st.button("🚀 Gelişim & Sertifikalar", help="Kendini nasıl geliştiriyor?"):
        st.session_state.prompt_input = "Ilgın kendini geliştirmek için neler yapıyor? Yeni stajı (Online Social Office), aldığı sertifikalar ve hobileri neler?"

with col6:
    if st.button("❤️ Sosyal Sorumluluk", help="Gunkoy Projesi Detayları"):
        st.session_state.prompt_input = "Gunkoy projesinde köy okulları için neler yaptı? Gece okulda kalıp boya yapması ve fiziksel katkıları gibi detayları anlat."

# Chat input (Manuel soru sorma)
user_question = st.chat_input("Veya buraya kendi sorunuzu yazın...")
if user_question:
    st.session_state.prompt_input = user_question

# Prompt'u değişkene alalım
prompt_input = st.session_state.get("prompt_input", None)

# ---- AI CEVAP MEKANİZMASI ----
if prompt_input and api_key:
    # Senin kullandığın yeni SDK yapısı
    client = genai.Client(api_key=api_key)
    MODEL_NAME = "gemini-2.0-flash" 

    # System Prompt: AI'a nasıl davranması gerektiğini söylüyoruz
    system_prompt = f"""
    Sen Ilgın Tandoğan'ı temsil eden profesyonel, samimi ve zeki bir AI asistanısın.
    Amacın, işverenlere Ilgın'ın hem teknik becerilerini hem de karakterini en iyi şekilde satmak/anlatmak.
    
    Aşağıdaki JSON verisini KESİNLİKLE temel al.
    Cevap verirken şu detayları vurgulamaya özen göster:
    - Portakal Technology'deki "şifresiz deployment" ve "multi-node" teknik detayları.
    - Gunkoy projesindeki "duvar boyama", "gece okulda kalma" gibi fedakarlık ve çalışkanlık detayları.
    - Özel ders verirken geliştirdiği "Adaptive Teaching" (Kişiye özel öğretim) yeteneği.
    
    Cevapların akıcı, motive edici ve Türkçe olsun.
    
    CV VERİSİ:
    {json.dumps(cv_data, ensure_ascii=False)}
    
    SORU:
    {prompt_input}
    """

    with st.spinner("Ilgın'ın hafızası taranıyor..."):
        try:
            # Yeni SDK Çağrısı
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=system_prompt
            )

            # Cevabı güvenli bir şekilde al
            answer = getattr(response, "text", None)
            if not answer:
                try:
                    answer = response.output[0].content[0].text
                except Exception:
                    answer = str(response)

            # Ekrana Yazdır
            st.markdown(f"**Soru:** {prompt_input}")
            st.markdown("---")
            st.markdown(answer)

            # Cevap bitince input'u temizle ki ekran saçmalamasın
            st.session_state.prompt_input = None

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
