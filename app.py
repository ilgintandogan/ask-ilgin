import streamlit as st
from openai import OpenAI
import json


st.set_page_config(page_title="Ilgın Tandoğan - Dijital İkiz", page_icon="🤖", layout="wide")

if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None


with st.sidebar:
    try:
        st.image("ilgin.jpg", caption="Ilgın Tandoğan", width=150)
    except:
        st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan")

    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](https://linkedin.com/in/ilgintandogan)")
    st.write("[GitHub](https://github.com/ilgintandogan)")

    api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("OpenAI API Key", type="password")


st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")
st.markdown("""
Ben, Ilgın'ın **CV verileri, proje deneyimleri ve kişisel özellikleriyle** eğitilmiş bir yapay zekâyım.  
Bana teknik, kariyer veya kişisel sorular sorabilirsin!
""")
st.markdown("---")


def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

cv_data = load_data()



col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)

with col1:
    if st.button("🍊 Portakal Tech Deneyimi"):
        st.session_state.prompt_input = "Ilgın Portakal Teknoloji stajında neler yaptı? Kubernetes, k0s, k0rdent ve ağ problemlerini detaylı anlat."

with col2:
    if st.button("🛠 Teknik Yetkinlikler"):
        st.session_state.prompt_input = "Ilgın'ın bildiği programlama dilleri, DevOps araçları ve cloud teknolojilerini listele."

with col3:
    if st.button("📚 Projeler (EduGraph, Web, Android)"):
        st.session_state.prompt_input = "Ilgın'ın EduGraph, WastlessWorld ve Android projelerini detaylandır."

with col4:
    if st.button("🧠 Karakter & Soft Skills"):
        st.session_state.prompt_input = "Ilgın'ın iş disiplini, güçlü yönleri ve soft skills özellikleri nelerdir?"

with col5:
    if st.button("🎓 Liderlik & Mentorluk"):
        st.session_state.prompt_input = "Ilgın'ın özel ders deneyimi ve mentorluk yaklaşımını açıkla."

with col6:
    if st.button("❤️ Günkoy Projesi"):
        st.session_state.prompt_input = "Ilgın'ın Günkoy projesindeki katkılarını detaylandır."

with col7:
    if st.button("🎯 Neden DevOps?"):
        st.session_state.prompt_input = "Ilgın neden DevOps alanına yöneldi? Kariyer vizyonu nedir?"

with col8:
    if st.button("💡 Zorluk & Çözüm Örneği"):
        st.session_state.prompt_input = "Ilgın'ın yaşadığı bir teknik problemi nasıl çözdüğünü örnekle anlat."

with col9:
    if st.button("🚀 Kişisel Gelişim Planı"):
        st.session_state.prompt_input = "Ilgın sertifikalar, hobiler ve kendini geliştirme açısından neler yapıyor?"



user_question = st.chat_input("Bir soru yaz…")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.prompt_input


if prompt_input and api_key:

    client = OpenAI(api_key=api_key)

    SYSTEM_PROMPT = f"""
    Sen Ilgın Tandoğan'ın kişisel dijital ikizisin.
    Profesyonel, samimi, akıcı ve güven veren bir üslupla cevap verirsin.

    Aşağıda Ilgın'ın CV verileri bulunmaktadır.
    Tüm cevaplarını bu verilere dayandır:

    {json.dumps(cv_data, ensure_ascii=False, indent=2)}

    Projeleri şu öncelikle anlat:
    1. BAYKOÇ (AI YKS Koçu)
    2. WastlessWorld (PHP/SQL)
    3. Android Studio projeleri

    Teknik detay sorulursa açıklayıcı ol.
    Kariyer sorulursa yönlendirici ol.
    Soft skills sorulursa motive edici ol.
    """

 
    status = st.empty()
    status.markdown("🤔 **Düşünüyorum… Lütfen bekleyin**")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_input}
            ]
        )

        answer = completion.choices[0].message.content

        status.empty()  

        st.markdown(f"### ❓ Soru: **{prompt_input}**")
        st.markdown("---")
        st.markdown(answer)

        st.session_state.prompt_input = None

    except Exception as e:
        status.empty()
        st.error(f"Bir hata oluştu: {e}")
