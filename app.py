import streamlit as st
from openai import OpenAI
import json

# Streamlit ayarları
st.set_page_config(page_title="Ilgın Tandoğan - Dijital İkiz", page_icon="🤖", layout="wide")

# Session
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

# Sidebar
with st.sidebar:
    try:
        st.image("ilgin.jpg", caption="Ilgın Tandoğan", width=150)
    except:
        st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan")

    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](https://www.linkedin.com/in/ilgintandogan) | [GitHub](https://github.com/ilgintandogan)")

    api_key = st.secrets.get("OPENAI_API_KEY", None) or st.text_input("OpenAI API Key", type="password")

# Başlık
st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")

st.markdown("""
Ben, Ilgın'ın **CV verileri, proje deneyimleri ve kariyer geçmişiyle** eğitilmiş kişisel bir yapay zekayım.  
Bana Ilgın hakkında teknik, kariyer, karakter ve proje soruları sorabilirsin!
""")
st.markdown("---")

# JSON data yükleme
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

try:
    cv_data = load_data()
except:
    st.error("data.json bulunamadı! GitHub'a yüklediğinden emin ol.")
    st.stop()

# ----------------------------------------------------------
# BUTONLAR (9'lu grid)
# ----------------------------------------------------------

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)

with col1:
    if st.button("🍊 Portakal Tech Deneyimi"):
        st.session_state.prompt_input = "Ilgın Portakal Teknoloji stajında ne yaptı? Kubernetes, k0s, k0rdent ve network sorunlarını örneklerle açıkla."

with col2:
    if st.button("🛠 Teknik Yetkinlikler"):
        st.session_state.prompt_input = "Ilgın'ın bildiği programlama dilleri, DevOps araçları ve cloud teknolojilerini detaylı listele."

with col3:
    if st.button("📚 Projeler"):
        st.session_state.prompt_input = "Ilgın'ın EduGraph, WastlessWorld ve Android projelerini detaylı açıkla."

with col4:
    if st.button("🧠 Karakter & Soft Skills"):
        st.session_state.prompt_input = "Ilgın'ın karakter özelliklerini, disiplinini ve çalışma tarzını açıkla."

with col5:
    if st.button("🎓 Liderlik & Mentorluk"):
        st.session_state.prompt_input = "Ilgın'ın özel ders tecrübesi ve mentorluk stilini açıkla."

with col6:
    if st.button("❤️ Sosyal Sorumluluk (Günkoy)"):
        st.session_state.prompt_input = "Ilgın'ın Günkoy projesinde yaptığı işleri ve katkılarını anlat."

with col7:
    if st.button("🎯 Neden DevOps?"):
        st.session_state.prompt_input = "Ilgın neden DevOps alanını seçti? Kariyer vizyonunu anlat."

with col8:
    if st.button("💡 Zorluk & Çözüm"):
        st.session_state.prompt_input = "Ilgın'ın teknik bir sorunla karşılaşıp çözdüğü bir örneği anlat."

with col9:
    if st.button("🚀 Kendini Nasıl Geliştiriyor?"):
        st.session_state.prompt_input = "Ilgın'ın sertifikaları, hobileri ve gelişim planını açıkla."

# ----------------------------------------------------------
# Manuel Soru
# ----------------------------------------------------------

user_question = st.chat_input("Bir soru yaz...")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.prompt_input

# ----------------------------------------------------------
# OpenAI API ile Yanıt Üretme
# ----------------------------------------------------------

if prompt_input and api_key:
    client = OpenAI(api_key=api_key)

    SYSTEM_PROMPT = f"""
Sen Ilgın Tandoğan'ın kişisel dijital ikizisin.

Görevlerin:
- Ilgın'ın CV verilerine dayanarak profesyonel, tutarlı ve etkileyici yanıtlar üret.
- İşverenlere yönelik güçlü açıklamalar yap.
- Teknik konuları örneklerle anlat.
- Projelerden özellikle şu sırayla bahset:
  1. EduGraph (AI YKS koçu)
  2. WastlessWorld (PHP/SQL web sistemi)
  3. Android Studio projeleri

CV verisi:
{json.dumps(cv_data, ensure_ascii=False)}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_input}
            ]
        )

        answer = completion.choices[0].message.content

        st.markdown(f"### ❓ Soru: {prompt_input}")
        st.markdown("---")
        st.markdown(answer)

        st.session_state.prompt_input = None

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
