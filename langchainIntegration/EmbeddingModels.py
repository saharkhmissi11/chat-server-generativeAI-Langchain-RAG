import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def embed_text(text):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    text_embedded = embeddings.embed_query(text)
    return text_embedded


def embed_doc(doc):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    doc_embedded = embeddings.embe
    return doc_embedded
