from models.document import Document
from repositories.documentRepo import DocumentRepo
from langchainIntegration.DocumentLoaders import load_pdf, load_website, load_docx, load_csv, load_youtube, load_HTML, load_image, load_pdff
from langchain_core.documents.base import Document as Doc


class DocumentService:
    def __init__(self):
        self.db = DocumentRepo()

    def get_all_documents(self):
        return self.db.read_all_documents()

    def create_document(self, document: Document):
        self.db.create_document(document)

    def get_document(self, document_id: int):
        return self.db.read_document(document_id)

    def update_document(self, document_id: int, document: Document):
        self.db.update_document(document_id, document)

    def delete_document(self, document_id: int):
        self.db.delete_document(document_id)

    def load_document(self, document_url: str) -> Doc:
        if document_url.endswith('.pdf'):
            loaded_content = load_pdf(document_url)
        elif document_url.endswith('.doc') or document_url.endswith('.docx'):
            loaded_content = load_docx(document_url)
        elif document_url.endswith('.csv'):
            loaded_content = load_csv(document_url)
        elif document_url.endswith('.jpg') or document_url.endswith('.png'):
            loaded_content = load_image(document_url)
        elif document_url.endswith('.html'):
            loaded_content = load_HTML(document_url)
        elif document_url.startswith('https://www.youtube.com/'):
            loaded_content = load_youtube(document_url)
        else:
            loaded_content = load_website(document_url)
        return loaded_content

    def to_string(self, doc: Doc) -> str:
        web_text = ""
        for page in doc:
            print(page.page_content)
            web_text += page.page_content + " "
        return web_text
