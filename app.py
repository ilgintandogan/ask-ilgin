import os
import json
import re
import streamlit as st
from datetime import datetime
from google import genai

st.set_page_config(page_title="Ilgın AI", page_icon="🤖", layout="wide")

DATA_DIR = "data"
ROOT_DATA_FILE = "data.json"
MODEL_NAME = "gemini-2.0-flash"

def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def load_all_data(data_dir=DATA_DIR, root_file=ROOT_DATA_FILE):
    parts = {}

    if os.path.isdir(data_dir):
        for fname in os.listdir(data_dir):
            if fname.endswith(".json"):
                key = fname.replace(".json", "")
                parts[key] = load_json_file(os.path.join(data_dir, fname))
        if parts:
            return parts

    if os.path.isfile(root_file):
        root = load_json_file(root_file)
        if isinstance(root, dict):
            parts["root"] = root
            return parts

    return {}

def text_from_part(part_key, part_value):
    chunks = []
    if isinstance(part_value, dict):
        for k, v in part_value.items():
            chunks.append({
                "id": k,
                "title": f"{part_key}/{k}",
                "text": json.dumps(v, ensure_ascii=False)
            })
    elif isinstance(part_value, list):
        for i, item in enumerate(part_value):
            chunks.append({
                "id": f"{part_key}_{i}",
                "title": part_key,
                "text": json.dumps(item, ensure_ascii=False)
            })
    else:
        chunks.append({
            "id": part_key,
            "title": part_key,
            "text": str(part_value)
