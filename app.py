import streamlit as st
import json
import os
import re
from difflib import SequenceMatcher

# ------- CONFIG -------
st.set_page_config(page_title="Ilgın - AI Asistanı", page_icon="🤖", layout="wide")

# ------- SESSION INIT -------
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None
if "history" not in st.session_state:
    st.session_state.history = []

# ------- UTIL: Load all json parts -------
DATA_DIR = "data"

def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def load_all_data(data_dir=DATA_DIR):
    parts = {}
    for fname in os.listdir(data_dir):
        if fname.endswith(".json"):
            key = fname.replace(".json", "")
            parts[key] = load_json_file(os.path.join(data_dir, fname))
    return parts

data_parts = load_all_data()

# If no data found stop
if not data_parts:
    st.error("Veri dosyaları bulunamadı. Lütfen `data/` klasörüne JSON dosyalarını yerleştirin.")
    st.stop()

# ------- SIMPLE RETRIEVAL: score chunks by token overlap -------
def text_from_part(part):
    # convert a JSON part to a list of searchable chunks
    chunks = []
    if not part:
        return chunks
    # handle dicts with known keys
    if isinstance(part, dict):
        for k, v in part.items():
            if isinstance(v, list):
                for item in v:
                    chunks.append({"id": item.get("id", k), "title": k, "text": json.dumps(item, ensure_ascii=False)})
            else:
                chunks.append({"id": k, "title": k, "text": json.dumps(v, ensure_ascii=False)})
    return chunks

all_chunks = []
for key, part in data_parts.items():
    all_chunks += text_from_part(part)

def token_overlap_score(query, text):
    q_tokens = set(re.findall(r"\w+", query.lower()))
    t_tokens = set(re.findall(r"\w+", text.lower()))
    if not q_tokens or not t_tokens:
        return 0.0
    overlap = q_tokens.intersection(t_tokens)
    return len(overlap) / max(1, len(q_tokens))

def retrieve_top_k(query, k=3):
    scored = []
    for c in all_chunks:
        score = token_overlap_score(query, c["text"])
        scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scored[:k] if s > 0]

# ------- SIDEBAR -------
with st.sidebar:
    profile = data_parts.get("profile", {}).get("profile", {})
    st.image("https://via.placeholder.com/150", caption=profile.get("name", "Ilgın"))
    st.markdown(f"**{profile.get('title','')}**")
    st.write(profile.get("location",""))
    contact = profile.get("contact", {})
    st.write(contact.get("email",""))
    st.write(f"[LinkedIn]({contact.get('linkedin','#')}) | [GitHub]({contact.get('github','#')})")
    api_key = st.secrets.get("GEMINI_API_KEY", None) or st.text_input("Google Gemini API Key", type="password")

# ------- MAIN UI -------
st.markdown("<style>.card{background:#f7f7f9;padding:12px;border-radius:10px;box-shadow:0 1px 2px rgba(0,0,0,0.05);}</style>", unsafe_allow_html=True)
st.title(f"Merhaba — {profile.get('name','')}'ın AI Asistanı")
st.write("CV verileriyle desteklenen, kısa ve açıklayıcı cevaplar almak için soru sor.")

col1, col2, col3 = st.columns(3)
if col1.button("🎓 Eğitim"):
    st.session_state.prompt_input = "Eğitim geçmişinden bahseder misin?"
if col2.button("🛠 Teknik Yetenekler"):
    st.session_state.prompt_input = "Hangi araçları ve teknolojileri biliyor?"
if col3.button("💼 Deneyim"):
    st.session_state.prompt_input = "DevOps ve Cloud deneyimlerinden özetle bahset."

user_question = st.chat_input("Ilgın hakkında ne merak ediyorsunuz?")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.get("prompt_input", None)

# ------- AI ANSWER MECHANISM -------
if prompt_input:
    if not api_key:
        st.warning("Lütfen önce API anahtarını giriniz.")
    else:
        # Retrieval: get top relevant chunks
        top_chunks = retrieve_top_k(prompt_input, k=4)
        # Build context string: include top chunks + short index
        context_text = ""
        sources = []
        for idx, c in enumerate(top_chunks, start=1):
            context_text += f"\n\n### Kaynak {idx}: {c['title']}\n{c['text']}"
            sources.append({"name": c["title"], "snippet": c["text"][:200]})

        # system prompt: daha açıklayıcı yanıtlar üretsin; kaynak göster.
        system_prompt = f"""
You are a helpful, professional assistant representing Ilgın Tandoğan's CV. Use the following extracted data snippets to answer the user's question in Turkish.
Be concise but explanatory: include short summary (1-3 cümle), then 2-4 detaylı madde, then "Kaynaklar" bölümünde hangi veri parçalarını kullandığını açıkça söyle.
If the answer cannot be found in the provided snippets, respond in Turkish that you don't know and direct to contact email: {contact.get('email','')}

User question: {prompt_input}

EXTRACTS:
{context_text}
"""

        # call Gemini
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            MODEL_NAME = "gemini-2.0-flash"
            with st.spinner("Cevap hazırlanıyor..."):
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
        except Exception as e:
            st.error(f"Model çağrısında hata: {e}")
            answer = None

        if answer:
            st.markdown("**Soru:** " + prompt_input)
            st.markdown("---")
            st.markdown(answer)

            # Show which sources were used (local)
            with st.expander("Kullanılan veri parçaları (kısa):", expanded=False):
                for s in sources:
                    st.write(f"- **{s['name']}** — {s['snippet']}...")

            # append to session history
            st.session_state.history.append({"q": prompt_input, "a": answer, "sources": sources})
            # reset prompt
            st.session_state.prompt_input = None

# ------- Show simple history -------
if st.session_state.history:
    st.write("---")
    st.subheader("Sohbet geçmişi")
    for i, item in enumerate(reversed(st.session_state.history[-6:]), start=1):
        st.markdown(f"**Soru {i}:** {item['q']}")
        st.markdown(f"{item['a']}")
