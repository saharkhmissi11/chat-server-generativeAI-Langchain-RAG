import os
import tempfile
import requests
import pdfplumber
import pandas as pd
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio
import aiohttp

async def fetch_pdf(session, url):
    async with session.get(url) as response:
        return await response.read()

async def load_pdf(url):
    async with aiohttp.ClientSession() as session:
        pdf_data = await fetch_pdf(session, url)
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, "temp_pdf.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf_data)
            async with pdfplumber.open(pdf_path) as pdf:
                tasks = [asyncio.ensure_future(extract_data(page)) for page in pdf.pages]
                await asyncio.gather(*tasks)

async def extract_data(page):
    # Extract text
    text = page.extract_text()

    # Extract tables
    tables = page.extract_tables()
    for table in tables:
        df = pd.DataFrame(table[1:], columns=table[0])
        # Process DataFrame...

    # Extract images
    images = page.to_images()
    for i, img in enumerate(images):
        img_path = f"image_{i}.png"
        img.save(img_path)
        # Process image...

async def main(urls):
    tasks = []
    async with ThreadPoolExecutor() as pool:
        for url in urls:
            task = asyncio.ensure_future(load_pdf(url))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    urls = ["url1", "url2"]  # List of URLs
    asyncio.run(main(urls))
