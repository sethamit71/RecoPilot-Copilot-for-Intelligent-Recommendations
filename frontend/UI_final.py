import streamlit as st
import requests
import pandas as pd
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "Tvh-demo/data_input"
#DATA_DIR = PROJECT_ROOT / "data_input"
CATALOG_FILE = DATA_DIR / "tvh_captioned_product.csv"
# Load catalog
catalog_df = pd.read_csv(CATALOG_FILE)
SEARCH_URL = "http://localhost:8000/search"

# --- Initialize session state ---
if "selected_ref" not in st.session_state:
    st.session_state.selected_ref = None
if "customer_id" not in st.session_state:
    st.session_state.customer_id = None

st.title("🔍 TVH Product Catalog Search")

query = st.text_input("Enter your query:", "I need warning labels for electrical hazards,it should be high voltage one")
customer_id_input = st.text_input("Enter your customer ID:", "8e5f5cf5-c450-4e10-8495-50a10172578b")

if st.button("Search", key="search_btn"):
    response = requests.post(SEARCH_URL, json={"query": query})
    data = response.json()

    st.subheader("Answer:")
    st.info(data.get("answer", "⚠️ No answer received"))

    st.subheader("Matching Products:")

    sources = data.get("sources", [])

    # --- helper function for recommend button ---
    def set_recommend(ref_id):
        st.session_state.selected_ref = ref_id
        st.session_state.customer_id = customer_id_input
        st.switch_page("pages/Recommendations.py")

    for i in range(0, len(sources), 4):
        cols = st.columns(4)
        for col, ref in zip(cols, sources[i:i+4]):
            ref_id = ref.get("ref_id")
            match = catalog_df[catalog_df["ref_id"] == ref_id]
            if not match.empty:
                row = match.iloc[0]
                with col:
                    if pd.notna(row["image_path"]):
                        st.image(
                            row["image_path"],
                            caption=f"REF: {row['ref_id']}",
                            use_container_width=True,
                        )
                        st.markdown(f"[🔗 View Product Page]({row['product_page']})")

                    st.write(f"**REF ID:** {row['ref_id']}")
                    st.write(f"**Description:** {row['description_gemini']}")

                    # ✅ Recommend button with callback
                    st.button(
                        f"🛒 Recommend",
                        key=f"rec_btn_{row['ref_id']}",
                        on_click=set_recommend,
                        args=(row['ref_id'],),  # pass current product id
                    )
