import os
from pathlib import Path

# Project root (automatically detect)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
print(PROJECT_ROOT)
# credentials
GEMINI_API_KEY="AIzaSyDLxvBSLXe2FX4EBBC4mU70zC-06PoKTjY"#<--2nd#"AIzaSyAmE4lZjj9hTIst3uxxHToIroKR7decGfs"
GEMINI_MODEL_NAME="gemini-1.5-flash"
OLLAMA_MODEL_NAME="llama3:8b"
OLLAMA_EMBEDDING_MODEL_NAME="nomic-embed-text"
# Data and output paths
DATA_DIR = PROJECT_ROOT / "data_input"
OUTPUT_DIR = PROJECT_ROOT / "data_output"

# Common files
CATALOG_FILE = DATA_DIR / "tvh_captioned_product.csv"
CUSTOMER_BOUGHT_FILE = DATA_DIR / "dummy_purchases - dummy_purchases.csv"


FAISS_INDEX = OUTPUT_DIR / "faiss_index.faiss"
BM25_INDEX = OUTPUT_DIR / "bm25_index.pkl"

# Models
OLLAMA_LLM_MODEL = "llama3:8b"
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"
GEMINI_LLM_MODEL=""

#NMF artifacts
NMF_W=OUTPUT_DIR/"nmf_W.pkl"
NMF_H=OUTPUT_DIR/ "nmf_H.pkl"
NMF_USER_INDEX=OUTPUT_DIR/"user_index.pkl"
NMF_PRODUCT_INDEX=OUTPUT_DIR/"product_index.pkl"
NMF_SIM_DF=OUTPUT_DIR/"sim_df.pkl"

WEIGHTS = [0.3, 0.7]  # weight for BM25 vs FAISS


