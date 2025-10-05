import streamlit as st
import requests
import pandas as pd
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
print(">>>>>>>>>>>>>>>>>>>",PROJECT_ROOT)
#DATA_DIR = PROJECT_ROOT / "Tvh-demo/data_input"
DATA_DIR = PROJECT_ROOT / "data_input"
CATALOG_FILE = DATA_DIR / "tvh_captioned_product.csv"
# Load catalog data
catalog_df = pd.read_csv(CATALOG_FILE)

RECOMMEND_URL = "http://localhost:8000/recommend"

# ✅ Ensure something was selected
if "selected_ref" not in st.session_state:
    st.error("⚠️ No product selected. Please go back to the search page.")
    st.stop()

ref_id = st.session_state.selected_ref
customer_id = st.session_state.customer_id

st.title(f"🛒 Recommendations for {ref_id}")
st.write("📤 Sending payload to /recommend:", {"ref_id": ref_id, "customer_id": customer_id})
print("📤 Sending payload to /recommend:", {"ref_id": ref_id, "customer_id": customer_id})
if st.button("⬅️ Back to Search"):
    st.switch_page("Home.py")

try:
    recs = requests.post(
        RECOMMEND_URL,
        json={"ref_id": ref_id, "customer_id": customer_id}
    ).json()

    for rec_id in recs.get("recommendations", []):
        rec_match = catalog_df[catalog_df["ref_id"] == rec_id]
        if not rec_match.empty:
            rec_row = rec_match.iloc[0]
            st.image(
                rec_row["image_path"],
                caption=f"REF: {rec_row['ref_id']}",
                use_container_width=True,
            )
            st.write(f"**Description:** {rec_row['description_gemini']}")
            st.markdown(f"[🔗 View Product Page]({rec_row['product_page']})")

except Exception as e:
    st.error(f"❌ Recommend API failed: {e}")
