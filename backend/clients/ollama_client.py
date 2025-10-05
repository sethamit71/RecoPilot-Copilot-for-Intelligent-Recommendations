from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from config.settings import OLLAMA_EMBEDDING_MODEL_NAME,OLLAMA_MODEL_NAME
llm = ChatOllama(model=OLLAMA_MODEL_NAME) 
EMBED_MODEL = OLLAMA_EMBEDDING_MODEL_NAME
embedding_model = OllamaEmbeddings(model=EMBED_MODEL)