from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, SeleniumURLLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.parsers.audio import OpenAIWhisperParserLocal
from langchain_core.documents.base import Document as Doc
from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders import parsers
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders.image import UnstructuredImageLoader
from langchain.document_loaders import Blob
from langchain.document_loaders.parsers.pdf import PDFPlumberParser
import pdfplumber
import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from spire.pdf.common import *
from spire.pdf import *
import tempfile
import os
import requests

def load_pdff(url):
    # extract text
    loader = PyPDFLoader(url)
    data = loader.load_and_split()
    return data

def load_pdf(url):
    # extract text
    loader = PyPDFLoader(url)
    data = loader.load_and_split()

    # extract tables
    with tempfile.TemporaryDirectory() as temp_dir:
        if(url.startswith("http")):
            pdf_path = os.path.join(temp_dir, "doc.pdf")
            with open(pdf_path, "wb") as f:
                response = requests.get(url)
                f.write(response.content)
        else:
            pdf_path = url
        with pdfplumber.open(pdf_path) as pdf:
            tables = []
            for page in pdf.pages:
                extracted_tables = page.extract_tables()
                if extracted_tables:
                    tables.extend(extracted_tables)

            for table in tables:

                for i in range(len(table)):
                    for j in range(len(table[i])):
                        table[i][j] = "" if table[i][j] is None else str(table[i][j])

                df = pd.DataFrame(table[1:], columns=table[0])
                loader1 = DataFrameLoader(df, page_content_column=df.columns[0])

                try:
                    donnees = loader1.load()  # Attempt to load data from DataFrameLoader

                    for d in donnees:
                        data.append(d)

                except Exception as e:
                    print(f"Error encountered in DataFrameLoader.load(): {e}")

    # extract images
        doc = PdfDocument()
        doc.LoadFromFile(pdf_path)
        for page_index in range(doc.Pages.Count):
            page = doc.Pages[page_index]
            images = []
            for image in page.ExtractImages():
                images.append(image)
            if images:
                index = 0
                for image in images:
                    image_filename = f'C:/Users/ASUS/Desktop/chat-server/images/extracted_page_{page_index}_image_{index}.png'
                    index += 1
                    image.Save(image_filename, ImageFormat.get_Png())
                    for d in load_image(image_filename):
                        if d.page_content != "":
                            data.append(d)
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


def load_youtube(url):
    import os
    os.environ["PATH"] = os.environ["PATH"] + os.pathsep + "C:/FFmpeg/bin"
    local = False
    urls = [url]
    save_dir = "C:/PFE"
    if local:
        loader = GenericLoader(
            YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParserLocal()
        )
    else:
        loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
    docs = loader.load()
    return docs

def load_HTML(url):
    loader = UnstructuredHTMLLoader(url)
    data = loader.load()
    return data

def load_image(url):
    loader = UnstructuredImageLoader(url)
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
    elif document_url.endswith('.html'):
        loaded_content = load_HTML(document_url)
    elif document_url.endswith('.jpg') or document_url.endswith('.png'):
        loaded_content = load_image(document_url)
    elif document_url.startswith('https://www.youtube.com/'):
        loaded_content = load_youtube(document_url)
    else:
        loaded_content = load_website(document_url)
    return loaded_content


def handle_nested_list(data):
    flat_list = []
    for item in data:
        # Check if item is a list (nested structure)
        if isinstance(item, list):
            # Recursively handle nested lists
            flat_list.extend(handle_nested_list(item))
        else:
            # Convert non-list items to strings (handle potential non-string elements)
            flat_list.append(str(item))
    return flat_list















