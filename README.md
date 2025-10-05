# 🚀 RecoPilot — Copilot for Intelligent Recommendations

## 🧭 Overview

**RecoPilot** is an AI-powered product recommendation and search engine that combines semantic understanding, user behavior, and hybrid retrieval to deliver context-aware, personalized suggestions in real time.  
This project solves the **findability problem** for an organization's catalog of labels & decals.

It enables users to:

- 🔍 Search for products in natural language (“battery hazard warning label 74mm yellow/black”)
- 🛒 Select a product from the results
- 🤝 View “Frequently Bought Together” recommendations based on purchase history (`customer_id + ref_id`)

---

## ⚙️ How to Run

1. **Create virtual environment** and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start backend APIs**  
   Inside `backend/` directory:
   ```bash
   uvicorn backend_app:app
   ```

3. **Start UI**  
   Inside `frontend/` directory:
   ```bash
   streamlit run UI_final.py
   ```

---

## 🧩 Data Preparation (Offline)

For this demo, we use a pre-processed dataset `tvh_captioned_product.csv` stored under `data_input/`.  
It was prepared from the original TVH catalog PDF using three offline steps:

- **Product size:** around 5k labels and decals  

### 1️⃣ Scraping & Parsing
Scripts under `data_scrapper/` extract raw product descriptions and metadata from the catalog and save as:
```
data_input/tvh_cat.csv
```

Product images are extracted and stored under:
```
frontend/output_images/
```

### 2️⃣ Description / Caption Generation
A GenAI script enriches raw descriptions (e.g., generating concise product captions with details such as size and color).

- Output saved as:
  ```
  data_input/tvh_captioned_product.csv
  ```
- For demo purposes, 72 product descriptions were generated (due to free GenAI quota).

⚡ *Note:* These scripts are included for completeness but are **not part of the live demo** to keep execution fast and reliable.

---

## 📂 Project Structure

```
tvh-demo/
│
├── backend/
│   ├── __init__.py
│   ├── backend_app.py                # FastAPI entrypoint (APIs: /search, /recommend)
│   │
│   ├── recommender/                  # RAG and Recommendation engines
│   │   ├── recommender_training.py   # NMF training
│   │   ├── nmf_recommender.py        # NMF model
│   │   └── rag_chain.py              # Retrieval-Augmented Generation logic
│   │
│   ├── clients/                      # Wrappers for external services
│   │   ├── ollama_client.py          # Local LLaMA client
│   │   ├── gemini_client.py          # Google Gemini client
│   │   └── __init__.py
│   │
│   ├── prompts/                      # Centralized prompt templates
│   │   ├── search_prompt.py
│   │   └── description_enrich_prompt.py
│   │
│   ├── config/
│   │   ├── settings.py               # Configs and model paths
│   │   └── logging.conf              # Logging setup
│   │
│   └── utils/
│       ├── file_utils.py
│       ├── text_cleaning.py
│       └── __init__.py
│
├── frontend/
│   └── ui.py                         # Streamlit UI (search + recommendations)
│
├── data_input/                       # Raw input data
│   ├── catalog.pdf
│   ├── tvh_captioned_product.csv
│   └── customer_bought.csv
│
├── data_output/                      # Processed/generated artifacts
│   ├── NMF_artifacts/
│   ├── faiss_index.faiss
│   ├── bm25_index.pkl
│   └── logs/
│
├── data_scrapper/
│   ├── text_cleaning.py
│   ├── data_scrapper_notebook.ipynb
│   ├── generate_caption_gemini.py
│
├── requirements.txt
└── README.md
```

---

## 🧠 Example Queries (Dashboard Arrows - Black/Grey)

**Scenario-style query:**  
“I need a dashboard decal that shows both left and right directions for a control lever.”  
→ Maps to **123TA4587** or **138TA1276** (bidirectional or multiple directions)

**Direct query:**  
“Show me the black on grey dashboard arrow that marks the neutral position.”  
→ Maps to **126TA9879**

**Functional query:**  
“Looking for a circular arrow label that indicates upward movement on a control panel.”  
→ Maps to **137TA9892**

**General description query:**  
“Do you have any dashboard arrow decals for diverging paths or split directions?”  
→ Maps to **138TA1652**

---

## 🎥 Demo Video

▶️ [Watch Demo Video](https://github.com/sethamit71/RecoPilot-Copilot-for-Intelligent-Recommendations/blob/main/tvh-demo.mkv)

---

✨ *Created by Amit Seth — AI Engineer | TRDDC TATA

