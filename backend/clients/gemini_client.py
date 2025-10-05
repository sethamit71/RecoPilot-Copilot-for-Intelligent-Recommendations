from config.settings import GEMINI_API_KEY, GEMINI_MODEL_NAME
# your retriever
import os
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL_NAME,
    temperature=0
)

