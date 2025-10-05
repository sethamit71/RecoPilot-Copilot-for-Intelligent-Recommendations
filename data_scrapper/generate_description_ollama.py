import pandas as pd
from typing import Optional

from langchain_community.llms import Ollama

# ===============================
# Configuration
# ===============================
CSV_IN = "tvh_cat.csv"
CSV_OUT = "tvh_cat_with_desc.csv"
USE_LLM = True
LLM_MODEL = "llama3.2"  # Lightweight model good for CPU + 16GB RAM

# ===============================
# Utility Functions
# ===============================
COLOR_MAP = {
    "BLACKB": "black",
    "BLACK": "black",
    "MIXEDW": "mixed white",
    "WHITE": "white",
    "YELLOW": "yellow",
    "RED": "red",
    "BLUE": "blue",
    "GREEN": "green",
}

def normalize_color(val: Optional[str]) -> str:
    if not val or str(val).strip().lower() in ("none", "nan", ""):
        return "unknown"
    return COLOR_MAP.get(str(val).strip().upper(), str(val).lower())

def fmt_dim(x) -> Optional[str]:
    if not x or str(x).strip().lower() in ("none", "nan", ""):
        return None
    return str(x).strip()

def dim_to_text(width, height, diameter) -> str:
    w = fmt_dim(width)
    h = fmt_dim(height)
    d = fmt_dim(diameter)
    if d and not (w or h):
        return f"round, diameter {d} mm"
    if w and h:
        return f"rectangular, {w}x{h} mm"
    if w:
        return f"width {w} mm"
    if h:
        return f"height {h} mm"
    return "size unspecified"

def rule_based_description(row: dict) -> str:
    fg = normalize_color(row.get("foreground"))
    bg = normalize_color(row.get("background"))
    size = dim_to_text(row.get("width"), row.get("height"), row.get("diameter"))
    cat = (row.get("category") or "label").replace("_", " ").strip()
    return f"{cat} label (ref {row.get('ref_id')}), {size}, {fg} on {bg}."

# ===============================
# LLM Setup
# ===============================
llm = None
if USE_LLM:
    try:
        llm = Ollama(model=LLM_MODEL)
        print("initialized LLM")
    except Exception as e:
        print(f"[WARN] Ollama init failed: {e}. Falling back to rule-based descriptions.")

def generate_description(row: dict) -> str:
    if llm:
        prompt = f"""
You are generating standardized product descriptions for TVH, a Belgium-based global supplier of parts and accessories for material handling, industrial, construction, and agricultural equipment.
Each product is described by the following attributes:
Fields:
ref_id: {row.get('ref_id')}
category: {row.get('category')}
foreground: {row.get('foreground')}
background: {row.get('background')}
width(mm): {row.get('width')}
height(mm): {row.get('height')}
diameter(mm): {row.get('diameter')}
Your task:
Write a concise technical description (1 sentences) suitable for the TVH website.

Guidelines:
1. Start by highlighting the product category.
2. Mention key dimensions (height, diameter).
3. Specify visual details (foreground elements, background colors).
4. Use professional, catalog-style language.
5. Ensure the style matches TVH’s existing product labels and decals.
Description:
"""
        try:
            print("invoking")
            resp = llm.invoke(prompt)
            return resp.strip()
        except Exception as e:
            print(f"[WARN] LLM generation failed: {e}")
    # fallback
    return rule_based_description(row)

# ===============================
# Main Ingestion Logic
# ===============================

df = pd.read_csv(CSV_IN).head(20)
print("data read")
enriched = []
for _, row in df.iterrows():
    print("started",_)
    row_dict = row.to_dict()
    row_dict["foreground"] = normalize_color(row_dict.get("foreground"))
    row_dict["background"] = normalize_color(row_dict.get("background"))
    print("genrating")
    desc = generate_description(row_dict)
    enriched.append(desc)

df["description"] = enriched
df.to_csv(CSV_OUT, index=False)
print(f"Generated descriptions and saved to `{CSV_OUT}`")


