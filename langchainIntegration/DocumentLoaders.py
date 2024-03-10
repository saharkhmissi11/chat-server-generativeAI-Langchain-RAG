from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, SeleniumURLLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.documents.base import Document as Doc
def load_pdf(url):
    loader = PyPDFLoader(url)
    data = loader.load_and_split()
    return data


def load_docx(url):
    loader = UnstructuredWordDocumentLoader(url)
    data = loader.load()
    return data


def load_website(url):
    loader = SeleniumURLLoader([url])
    data = loader.load()
    return data


def load_csv(url):
    loader = CSVLoader(file_path=url)
    data = loader.load()
    return data


def to_string(docs: Doc) -> str:
    web_text = ""
    for page in docs:
        print(page.page_content)
        web_text += page.page_content + " "
    return web_text


def load_document(document_url: str) -> list[Doc]:
    if document_url.endswith('.pdf'):
        loaded_content = load_pdf(document_url)
    elif document_url.endswith('.doc') or document_url.endswith('.docx'):
        loaded_content = load_docx(document_url)
    elif document_url.endswith('.csv'):
        loaded_content = load_csv(document_url)
    else:
        loaded_content = load_website(document_url)
    return loaded_content
