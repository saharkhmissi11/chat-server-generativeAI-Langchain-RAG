from fastapi import FastAPI
from controllers.documentController import router as document_router



app = FastAPI()

app.include_router(document_router)

