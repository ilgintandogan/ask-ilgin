# app.py
# Interactive resume assistant (Streamlit)
# - supports either ./data/*.json files OR a single ./data.json
# - simple token-overlap retrieval + Google Gemini model call
# - creates a sample data/profile.json for quick dev if none provided

import os
import re
import json
import streamlit as st

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Ilgın - AI Asistanı", page_icon="🤖", layout="wide")

DATA_DIR = "data"
ROOT_DATA_FILE = "data.json"
MODEL_NAME_DEFAULT = "gemini-2.0-flash"

# ----------------- HELPERS -----------------
def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"JSON yükleme hatası: {path} — {e}")
        return None

def ensure_sample_data(data_dir=DATA_DIR):
    """Create a sample profile.json if no data present (development helper)."""
    os.makedirs(data_dir, exist_ok=True)
    sample = {
        "profile": {
            "name": "Ilgın Tandoğan",
            "title": "CTIS Student & DevOps Enthusiast",
            "location": "Ankara, Türkiye",
            "contact": {"email": "ilgintandogan@gmail.com"},
            "summary": "Bilkent CTIS öğrencisi. DevOps, Kubernetes, k0s deneyimi."
        }
    }
    sample_path = os.path.join(data_dir, "profile.json")
    if not os.path.isfile(sample_path):
        with open(sample_path, "w", encoding="utf-8") as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)
    return sample

def load_all_data(data_dir=DATA_DIR, root_file=ROOT_DATA_FILE):
    parts = {}

    # Debug info (temporary — can remove)
    try:
        st.write("Çalışma dizini:", os.getcwd())
        st.write("Kök dizin dosyaları (örnek):", os.listdir("."))
    except Exception:
        pass

    # Case A: folder with JSON parts
    if os.path.isdir(data_dir):
        files = [f for f in os.listdir(data_dir) if f.lower().endswith(".json")]
        if files:
            for fname in files:
                key = fname.replace(".json", "")
                path = os.path.join(data_dir, fname)
                parts[key] = load_json_file(path)
            return parts

    # Case B: single root data.json
    if os.path.isfile(root_file):
        root_data = load_json_file(root_file)
        if isinstance(root_data, dict):
            # try to detect common keys and split logically, otherwise store as 'root'
            parts["root"] = root_data
            return parts
        else:
            st.error(f"'{root_file}' beklenen JSON yapısında değil.")
            return parts

    # Case C: nothing found — create sample for dev and return it
    sample = ensure_sample_data(data_dir)
    parts.update(sample)
    st.info(f"'{data_dir}/' klasörü bulunamadı veya boştu; örnek dosya oluşturuldu ({data_dir}/profile.json).")
    return parts

# ----------------- RETRIEVAL: convert loaded parts to searchable chunks -----------------
def text_from_part(part_key, part_value):
    chunks = []
    if part_value is None:
        return chunks
    if isinstance(part_value, dict):
        for k, v in part_value.items():
            if isinstance(v, list):
                for item in v:
                    title = f"{part_key}/{k}"
                    text = json.dumps(item, ensure_ascii=False)
                    chunks.append({"id": item.get("id", title) if isinstance(item, dict) else title, "title": title, "text": text})
            else:
                title = f"{part_key}/{k}"
                text = json.dumps(v, ensure_ascii=False)
                chunks.append({"id": k, "title": title, "text": text})
    elif isinstance(part_value, list):
        for item in part_value:
            title = f"{part_key}"
            text = json.dumps(item, ensure_ascii=False)
            chunks.append({"id": getattr(item, "get", lambda *_: title)(), "title": title, "text": text})
    else:
        chunks.append({"id": part_key, "title": part_key, "text": json.dumps(part_value, ensure_ascii=False)})
    return chunks

def token_overlap_score(query, text):
    q_tokens = set(re.findall(r"\w+", query.lower()))
    t_tokens = set(re.findall(r"\w+", text.lower()))
    if not q_tokens:
        return 0.0
    overlap = q_tokens.intersection(t_tokens)
    return len(overlap) / max(1, len(q_tokens))

def retrieve_top_k(query, chunks, k=4):
    scored = []
    for c in chunks:
        score = token_overlap_score(query, c["text"])
        scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scored[:k] if s > 0]

# ----------------- STREAMLIT UI -----------------
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None
if "history" not in st.session_state:
    st.session_state.history = []

data_parts = load_all_data()
if not data_parts:
    st.error("Veri yüklenemedi. 'data/' klasörünü veya 'data.json' dosyasını kontrol edin.")
    st.stop()

# Sidebar: profile + API key
with st.sidebar:
    profile = (data_parts.get("profile") or data_parts.get("root", {}).get("profile") or {})
    st.image("https://via.placeholder.com/150", caption=profile.get("name", "Ilgın"))
    st.markdown(f"**{profile.get('title','')}**")
    st.write(profile.get("location", ""))
    contact = profile.get("contact", {})
    if contact:
        st.write(contact.get("email", ""))
        st.write(f"[LinkedIn]({contact.get('linkedin','#')}) | [GitHub]({contact.get('github','#')})")
    api_key = st.secrets.get("GEMINI_API_KEY", None) or st.text_input("Google Gemini API Key", type="password")

st.markdown("<div style='padding:6px;border-radius:10px;background:#f6f7fb'>"
            f"<h2>Merhaba — {profile.get('name','')}'ın AI Asistanı</h2>"
            "<p>CV verilerine dayanarak kısa ve açıklayıcı cevaplar alabilirsiniz.</p></div>", unsafe_allow_html=True)

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

# ----------------- ANSWER MECHANISM -----------------
if prompt_input:
    if not api_key:
        st.warning("Lütfen önce API anahtarını giriniz.")
    else:
        # prepare chunks
        all_chunks = []
        for key, val in data_parts.items():
            all_chunks += text_from_part(key, val)

        top_chunks = retrieve_top_k(prompt_input, all_chunks, k=4)
        context_text = ""
        sources = []
        for idx, c in enumerate(top_chunks, start=1):
            context_text += f"\n\n### Source {idx}: {c['title']}\n{c['text']}"
            sources.append({"name": c["title"], "snippet": c["text"][:200]})

        system_prompt = f"""
You are a helpful, professional assistant representing Ilgın Tandoğan's CV. Use the following data snippets to answer the user's question in Turkish.
Answer format:
- Very short summary (1-2 sentences)
- 2-4 bullet points with details
- 'Kaynaklar' section listing which data parts were used.

If the answer is not present in the provided snippet
