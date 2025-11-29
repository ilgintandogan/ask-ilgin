import os
import re
import json
import streamlit as st

st.set_page_config(page_title="Ilgın - AI Asistanı", page_icon="🤖", layout="wide")

DATA_DIR = "data"
ROOT_DATA_FILE = "data.json"
MODEL_NAME_DEFAULT = "gemini-2.0-flash"

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

    sample = {
        "profile": {
            "name": "Ilgın Tandoğan",
            "title": "CTIS Student & DevOps Enthusiast",
            "location": "Ankara, Türkiye",
            "contact": {"email": "ilgintandogan@gmail.com"},
            "summary": "Bilkent CTIS öğrencisi. DevOps ve Kubernetes deneyimi."
        }
    }

    if not os.path.isfile(sample_path):
        with open(sample_path, "w", encoding="utf-8") as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)

    return {"profile": sample["profile"]}

def load_all_data(data_dir=DATA_DIR, root_file=ROOT_DATA_FILE):
    parts = {}

    if os.path.isdir(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
        if files:
            for fname in files:
                key = fname.replace(".json", "")
                parts[key] = load_json_file(os.path.join(data_dir, fname))
            return parts

    if os.path.isfile(root_file):
        root_data = load_json_file(root_file)
        if isinstance(root_data, dict):
            parts["root"] = root_data
            return parts

    return ensure_sample_data()

def text_from_part
