import os
import re
import json
import streamlit as st

# -----------------------------------------------------------
# CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Ilgın - AI Asistanı", page_icon="🤖", layout="wide")

DATA_DIR = "data"
ROOT_DATA_FILE = "data.json"
MODEL_NAME_DEFAULT = "gemini-2.0-flash"


# -----------------------------------------------------------
# HELPERS
# -----------------------------------------------------------
def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"JSON yükleme hatası: {path} — {e}")
        return None


def ensure_sample_data(data_dir=DATA_DIR):
    os.makedirs(data_dir, exist_ok=True)
    sample_path = os.path.join(data_dir, "profile.json")

    if not os.path.isfile(sample_path):
        sample = {
            "profile": {
                "name": "Ilgın Tandoğan",
                "title": "CTIS Student & DevOps Enthusiast",
                "location": "Ankara, Türkiye",
                "contact": {"email": "ilgintandogan@gmail.com"},
                "summary": "Bilkent CTIS öğrencisi. DevOps ve Kubernetes deneyimi."
            }
        }
        with open(sample_path, "w", encoding="utf-8") as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)

    return {"profile": sample}


def load_all_data(data_dir=DATA_DIR, root_file=ROOT_DATA_FILE):
    parts = {}

    # Case A: folder with JSON files
    if os.path.isdir(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
        if files:
            for fname in files:
                key = fname.replace(".json", "")
                parts[key] = load_json_file(os.path.join(data_dir, fname))
            return parts

    # Case B: single root data.json
    if os.path.isfile(root_file):
        root_data = load_json_file(root_file)
        if isinstance(root_data, dict):
            parts["root"] = root_data
            return parts

    # Case C: nothing exists → create sample
    return ensure_sample_data()


def text_from_part(part_key, part_value):
    chunks = []
    if isinstance(part_value, dict):
        for k, v in part_value.items():
            title = f"{part_key}/{k}"
            chunks.append({"id": k, "title": title, "text": json.dumps(v, ensure_ascii=False)})
    return chunks


def token_overlap_score(query, text):
    q_tokens = set(re.findall(r"\w+", query.lower()))
    t_tokens = set(re.findall(r"\w+", text.lower()))
    return len(q_tokens.intersection(t_tokens)) / max(1, len(q_tokens))


def retrieve_top_k(query, chunks, k=4):
    scored = [(token_overlap_score(query, c["text"]), c) for c in chunks]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scored[:k] if s > 0]


# -----------------------------------------------------------
# STREAMLIT START
# -----------------------------------------------------------
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

if "history" not in st.session_state:
    st.session_state.history = []

data_parts = load_all_data()
profile = data_parts.get("profile") or data_parts.get("root", {}).get("profile") or {}


# -----------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption=profile.get("name", "Ilgın"))
    st.markdown(f"**{profile.get('title','')}**")
    st.write(profile.get("location", ""))

    contact = profile.get("contact", {})
    if contact:
        st.write(contact.get("email", ""))

    api_key = (
        st.secrets.get("GEMINI_API_KEY", None)
        or st.text_input("Google Gemini API Key", type="password")
    )


# -----------------------------------------------------------
# MAIN UI
# -----------------------------------------------------------
st.markdown(
    "<h2>Ilgın'ın AI Asistanı</h2><p>CV verisine dayalı hızlı cevaplar verir.</p>",
    unsafe_allow_html=True,
)

user_question = st.chat_input("Ilgın hakkında ne merak ediyorsun?")
if user_question:
    st.session_state.prompt_input = user_question

prompt_input = st.session_state.prompt_input


# -----------------------------------------------------------
# ANSWER HANDLER
# -----------------------------------------------------------
if prompt_input:
    if not api_key:
        st.warning("API anahtarı gerekli.")
        st.stop()

    chunks = []
    for key, val in data_parts.items():
        chunks += text_from_part(key, val)

    top = retrieve_top_k(prompt_input, chunks)
    context_text = "\n\n".join([c["text"] for c in top])
    sources = ", ".join([c["title"] for c in top])

    # !!! Kritk düzeltme: Üçlü tırnak içinde süslü parantez YOK !!!
    system_prompt_template = """
Sen Ilgın
