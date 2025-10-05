Overview
RecoPilot is an AI-powered product recommendation and search engine that combines semantic understanding, user behavior, and hybrid retrieval to deliver context-aware, personalized suggestions in real time.
This project solves the findability problem for an organizations catalog of labels & decals.
It enables users to:

- Search for products in natural language (“battery hazard warning label 74mm yellow/black”).

- Select a product from the results.

-View “Frequently Bought Together” recommendations based on purchase history (customer_id + ref_id).


How to run:
create venv and install requirement.txt
start backend APIs: inside backend directory run to update FastAPI :uvicorn backend_app:app
start UI screen   :   inside frontend  directory run                  :streamlit run UI_final.py



Data Preparation (Offline)

For this demo, we are using a pre-processed dataset (tvh_captioned_product.csv) stored under data_input/.
This dataset was prepared from the original TVH catalog PDF using three offline steps:
Product size: around 5k for lables and decals

1.Scraping & Parsing

Scripts under data_scrapper/ extract raw product descriptions and metadata from the catalog. and saved as data_input/tvh_cat.csv
3.extract images of product
   all th eimages are saved in frontend/output_images/

2.Description / Caption Generation

A GenAI script enriches the raw descriptions (e.g., generating concise product captions with foreground/background/size).

   -The output is saved as a structured CSV: data_input/tvh_captioned_product.csv.
   - for demo purpoe i have generated 72 products description(due free gen=mini quota)

⚡ Note: These scripts are included in the repo for completeness, but they are not part of the live demo flow to keep things fast and reliable.

project stucture

tvh-demo/
│
├── backend/
│   ├── __init__.py
│   ├── backend_app.py        # FastAPI entrypoint (APIs: /search, /recommend)
│   │
│   │
│   ├── recommender/          # Rag and Recommendation engines
│   │   ├── recommender_training.py  # NMF training
│   │   ├── nmf_recommender.py       # NMF
│   │   └── rag_chain.py           # Retrieval-Augmented Generation logic
│   │
│   ├── clients/              # Wrappers for external services
│   │   ├── ollama_client.py  # Local LLaMA client
│   │   ├── gemini_client.py  # Google Gemini client
│   │   └── __init__.py
│   │
│   ├── prompts/              # Centralized prompt templates
│   │   ├── search_prompt.py  # JSON answer format for catalog
│   │   └── description_enrich_prompt.py     # to create description
│   │
│   ├── config/               # Configurations
│   │   ├── settings.py       # File paths, model configs
│   │   └── logging.conf      # Logging setup
│   │
│   └── utils/                # Helper utilities (optional)
│       ├── file_utils.py
│       ├── text_cleaning.py
│       └── __init__.py
│
├── frontend/
│   └── ui.py                 # Streamlit UI (search + recommendations)
│
├── data_input/               # Raw input data
│   ├── catalog.pdf
│   ├── tvh_captioned_product.csv
│   └── customer_bought.csv
│
├── data_output/              # Processed/generated artifacts
│   ├── NMF artifacts
│   ├── faiss_index.faiss
│   ├── bm25_index.pkl
│   ├── 
│   └── logs/
│
├── data_scrapper
│   ├── text_cleaning.py
│   ├── data_scrapper notebook
│   ├── generate_caption_gemini.py    # notebook/script to scrape raw catalog and description enrichment
│
|                  │
├── requirements.txt
└── README.md


Example Queries for Dashboard Arrows (Black/Grey)

Scenario-style query:
“I need a dashboard decal that shows both left and right directions for a control lever.”
→ Should map to 123TA4587 or 138TA1276 (bidirectional or multiple directions).

Direct query:
“Show me the black on grey dashboard arrow that marks the neutral position.”
→ Should map to 126TA9879 (arrow with “N”).

Functional query:
“Looking for a circular arrow label that indicates upward movement on a control panel.”
→ Should map to 137TA9892.

General description query:
“Do you have any dashboard arrow decals for diverging paths or split directions?”
→ Should map to 138TA1652 (diverging paths)



