
from typing import List, Callable
from pydantic import Field
from langchain.prompts import PromptTemplate
from fastapi import FastAPI, Query
from langchain.chains import RetrievalQA
from recommender.rag_chain import ensemble
from pydantic import BaseModel 
app = FastAPI(title="TVH Catalog Search API")
from recommender.rag_chain import qa_chain

# FastAPI app
class QueryRequest(BaseModel):
    query: str

@app.post("/search")
def search_products(request: QueryRequest):
    result = qa_chain({"query": request.query})
    return {
        "answer": result["result"],
        "sources": [doc.metadata for doc in result["source_documents"]]
    }    
from recommender.nmf_ecommender import recommend
class RecommenderRequest(BaseModel):
    customer_id: str
    ref_id: str
@app.post("/recommend")
def search_products(request: RecommenderRequest):
    result = recommend(customer_id=request.customer_id, product_id="REF"+" "+request.ref_id, top_n=5, alpha=0)
    print(" recommend result>>>>>>>",result)
    return {
        "recommendations": [i.split()[1] for i in result.index.tolist()],
        "scores": result.values.tolist()
    }

