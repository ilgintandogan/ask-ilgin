import streamlit as st
from openai import OpenAI
import json

# --- Streamlit Page Config ---
st.set_page_config(page_title="Ilgın Tandoğan - Dijital İkiz", page_icon="🤖", layout="wide")

# --- Session State ---
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

# --- Sidebar ---
with st.sidebar:
    try:
        st.image("ilgin.jpg", caption="Ilgın Tandoğan", width=150)
    except:
        st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan")

    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](http://www.linkedin.com/in/ilgintandogan) | [GitHub](https://github.com/ilgintandogan)")

    api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("OpenAI API Key", type="password")

# --- Başlık ---
st.title("Merhaba! Ben Ilgın'ın Dijital İkiziyim 👋")
st.markdown("""
Ben, Ilgın'ın **CV verileri, proje deneyimleri, kişisel özellikleri ve kariyer hedefleriyle** eğitilmiş bir yapay zekâyım.
Ilgın hakkında merak ettiğin her şeyi sorabilirsin.
""")
st.markdown("---")

# --- JSON Veri Yükleme ---
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

cv_data = load_data()

# --- Kullanıcı girişi ---
user_question = st.chat_input("Bir soru yaz…")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.get("prompt_input")

# --- AI Cevap Motoru ---
if prompt_input and api_key:
    client = OpenAI(api_key=api_key)

    # SYSTEM PROMPT → Ilgın’ın karakteri + CV verileri + uygulama persona
    system_prompt = f"""
    Sen Ilgın Tandoğan'ın dijital ikizisin.
    Profesyonel, samimi, motive edici ve açıklayıcı bir tarzda konuşursun.

    Aşağıda Ilgın’ın tüm CV verileri bulunmaktadır.
    Bu verileri mutlaka cevaplarında kullan.

    CV VERİLERİ:
    {json.dumps(cv_data, ensure_ascii=False, indent=2)}

    Kurallar:
    - Ilgın gibi davran.
    - Teknik konuları gerektiğinde sade ve net açıkla.
    - Sorulan soruya göre kariyer danışmanı, mentor veya teknik anlatıcı gibi cevap ver.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # hızlı + ucuz + çok kaliteli
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_input}
            ]
        )

        answer = response.choices[0].message.content

        st.markdown(f"### ❓ Soru:  
**{prompt_input}**  
")
        st.markdown("---")
        st.write(answer)

        # soruyu sıfırla
        st.session_state.prompt_input = None

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
