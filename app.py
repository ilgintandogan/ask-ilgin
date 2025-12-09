import streamlit as st
from openai import OpenAI
import json

# ---- Streamlit Ayarları ----
st.set_page_config(page_title="Ilgın Tandoğan - Dijital İkiz", page_icon="🤖", layout="wide")

if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

# ---- Sidebar ----
with st.sidebar:
    try:
        st.image("ilgin.jpg", caption="Ilgın Tandoğan", width=150)
    except:
        st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan")

    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](https://linkedin.com/in/ilgintandogan)")
    st.write("[GitHub](https://github.com/ilgintandogan)")

    # OpenAI API Key
    api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("OpenAI API Key", type="password")

# ---- Başlık ----
st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")
st.markdown("""
Ben, Ilgın'ın **CV verileri, projeleri ve kişisel özellikleriyle** eğitilmiş bir yapay zekâyım.  
Teknik yetkinlikleri, projeleri ve kariyer hedefleri hakkında bana soru sorabilirsin.
""")
st.markdown("---")

# ---- CV JSON Yükleme ----
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

cv_data = load_data()

# ---- Kullanıcı Input ----
user_question = st.chat_input("Bir soru yaz…")

if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.get("prompt_input")

# ---- OpenAI Cevap Motoru ----
if prompt_input and api_key:

    client = OpenAI(api_key=api_key)

    system_prompt = f"""
    Sen Ilgın Tandoğan'ın dijital ikizisin.
    Profesyonel, samimi, enerjik ve motive edici bir üslupla konuşursun.

    Aşağıda Ilgın'ın CV verileri yer alıyor.
    Bu verileri mutlaka cevaplarında kullan ve Ilgın'ın becerilerini öne çıkar:

    CV VERİLERİ:
    {json.dumps(cv_data, ensure_ascii=False, indent=2)}

    Kurallar:
    - Sorulan soruya göre teknik veya kişisel açıklama yap.
    - Cevaplar çok uzun olmasın; net, akıcı ve öz olsun.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_input}
            ]
        )

        answer = response.choices[0].message.content

        st.markdown(f"### ❓ Soru:\n**{prompt_input}**")
        st.markdown("---")
        st.write(answer)

        st.session_state.prompt_input = None

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
