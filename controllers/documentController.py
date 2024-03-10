from fastapi import APIRouter, Body, HTTPException
from models.document import Document
from services.documentService import DocumentService
from langchainIntegration.EmbeddingModels import embed_text, embed_doc
from langchain_core.documents.base import Document as Doc
from langchainIntegration.Redis import load, similarity_search, retrieve

router = APIRouter()
document_service = DocumentService()


@router.post("/embed")
async def embed(text: str):
    return embed_text(text)


@router.post("/redis")
async def redis(request_body: dict = Body(...)):
    try:
        document_url = request_body.get("document_url")
        load(document_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retrieve/{question}")
async def ret(question: str):
    return retrieve(question)


@router.post("/search/{query}")
async def create_document(query: str):
    return similarity_search(query)


@router.post("/documents/")
async def create_document(document: Document):
    document_service.create_document(document)
    return document


@router.get("/documents/{document_id}")
async def read_document(document_id: int):
    document = document_service.get_document(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.put("/documents/{document_id}")
async def update_document(document_id: int, document: Document):
    document_service.update_document(document_id, document)
    return {"message": "Document updated successfully"}


@router.delete("/documents/{document_id}")
async def delete_document(document_id: int):
    document_service.delete_document(document_id)
    return {"message": "Document deleted successfully"}


@router.post("/documents")
async def load_document(request_body: dict = Body(...)):
    try:
        document_url = request_body.get("document_url")
        loaded_document = document_service.load_document(document_url)
        return loaded_document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/docs")
async def load_document(request_body: dict = Body(...)):
    try:
        document_url = request_body.get("document_url")
        loaded_document = document_service.load_document(document_url)
        return document_service.to_string(loaded_document)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

