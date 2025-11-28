# app.py
import streamlit as st
from google import genai
import json

st.set_page_config(page_title="Ilgın Tandoğan - AI Asistanı", page_icon="🤖")

# ---- SESSION STATE INIT ----
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="Ilgın Tandoğan")
    st.write("📍 Ankara, Türkiye")
    st.write("📧 ilgintandogan@gmail.com")
    st.write("[LinkedIn](http://www.linkedin.com/in/ilgintandogan) | [GitHub](https://github.com/ilgintandogan)")
    # API Key alma: önce secrets sonra input
    api_key = st.secrets.get("GEMINI_API_KEY", None) or st.text_input("Google Gemini API Key", type="password")

# --- ANA EKRAN ---
st.title("Merhaba! Ben Ilgın'ın AI Asistanıyım 👋")
st.write("""
Ben Ilgın'ın CV verileriyle eğitilmiş bir yapay zekayım. 
Bana onun **DevOps tecrübeleri, projeleri, sertifikaları veya eğitimi** hakkında soru sorabilirsiniz.
""")

# Load JSON
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

try:
    cv_data = load_data()
except FileNotFoundError:
    st.error("data.json dosyası bulunamadı!")
    st.stop()

# Hazır sorular (butonlar) -- bunlar session_state'i set eder
col1, col2, col3 = st.columns(3)
if col1.button("🎓 Eğitimi nedir?"):
    st.session_state.prompt_input = "Eğitim geçmişinden bahset."
if col2.button("🛠 Hangi araçları biliyor?"):
    st.session_state.prompt_input = "Teknik yetkinlikleri ve bildiği araçlar neler?"
if col3.button("💼 DevOps deneyimi var mı?"):
    st.session_state.prompt_input = "DevOps ve Cloud alanındaki deneyimlerinden bahset."

# Chat input
user_question = st.chat_input("Ilgın hakkında ne merak ediyorsunuz?")
if user_question:
    st.session_state.prompt_input = user_question

# Güvenli okuma: prompt_input burada her zaman tanımlı (None ya da string)
prompt_input = st.session_state.get("prompt_input", None)

# ---- AI CEVAP MEKANİZMASI ----
if prompt_input and api_key:
    client = genai.Client(api_key=api_key)
    MODEL_NAME = "gemini-2.0-flash"  # Hesabında erişimin varsa değiştirebilirsin

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
            # SDK sürümüne göre response yapısı değişebilir; .text sık çalışır
            answer = getattr(response, "text", None)
            if not answer:
                # fallback: daha derin yapılar
                try:
                    answer = response.output[0].content[0].text
                except Exception:
                    answer = str(response)

            st.markdown(f"**Soru:** {prompt_input}")
            st.markdown("---")
            st.markdown(answer)

            # Eğer yanıt verildikten sonra prompt'u temizlemek istersen:
            st.session_state.prompt_input = None

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

elif prompt_input and not api_key:
    st.warning("Lütfen önce API anahtarını giriniz.")
