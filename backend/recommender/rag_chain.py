import pandas as pd
from typing import List, Dict, Optional, Any
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.tools import tool
from langchain.chains import RetrievalQA
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from clients.ollama_client import embedding_model
from clients.gemini_client import llm

# ----------------------------
from config.settings import CATALOG_FILE,FAISS_INDEX,BM25_INDEX,WEIGHTS
from prompts.search_prompts import search_template

# ----------------------------
# Load Data
# ----------------------------
df = pd.read_csv(CATALOG_FILE)
#texts = df["description"].astype(str).tolist()
df["text"] = (
    "REF " + df["ref_id"].astype(str) + ", category " + df["category"].astype(str) +
    ", sub-category " + df["sub-category"].astype(str) +
    ", foreground " + df["foreground"].astype(str) +
    ", background " + df["background"].astype(str) +
    ", width " + df["width"].astype(str) + " mm, height " + df["height"].astype(str) +
    ", description " + df["description_gemini"].astype(str)
)
texts = df["text"].astype(str).tolist()
ids = df["ref_id"].astype(str).tolist()
metas = df.drop(columns=["description_gemini"]).to_dict(orient="records")
# ----------------------------
# Load or Create FAISS VectorStore
# ----------------------------
if os.path.exists(FAISS_INDEX):
    print("✅ Loading existing FAISS index...")
    faiss_store = FAISS.load_local(
        FAISS_INDEX,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True  # required by LangChain 0.2+
    )
else:
    print("⚡ Creating new FAISS index...")
    faiss_store = FAISS.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metas,
        ids=ids
    )
    faiss_store.save_local(FAISS_INDEX)
    print(f"💾 Saved FAISS index to {FAISS_INDEX}")

if os.path.exists(BM25_INDEX):
    with open(BM25_INDEX, "rb") as f:
        bm25 = pickle.load(f)
    print("✅ Loaded existing BM25 index")
else:
    bm25 = BM25Retriever.from_texts(texts, metadatas=metas)
    bm25.k = 5
    with open(BM25_INDEX, "wb") as f:
        pickle.dump(bm25, f)
    print(">>> Created and saved new BM25 index")

# Dense Retriever: FAISS

faiss_retriever = faiss_store.as_retriever(search_kwargs={"k": 5})

# Ensemble Retriever (Hybrid)

ensemble = EnsembleRetriever(
    retrievers=[bm25, faiss_retriever],
    weights=WEIGHTS
)
prompt = PromptTemplate(
    template=search_template,
    input_variables=["context", "question"]
)
#Create the QA chain using your ensemble retriever
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=ensemble,
    return_source_documents=True,
    chain_type="stuff",  # combines all docs into one prompt
    chain_type_kwargs={"prompt": prompt}  # pass custom prompt here
)
