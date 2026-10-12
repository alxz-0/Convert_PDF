from pdf2docx import Converter
from PIL import Image

import pandas as pd
import os
import pymupdf

# PDF to TXT
def pdf_to_txt(pdf_path, output_folder):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output = os.path.join(output_folder, f"{filename}.txt")
    
    doc = pymupdf.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    with open(output, "w", encoding="utf-8") as f:
        f.write(text)
    doc.close()

# PDF to XLSX
def pdf_to_xlsx(pdf_path, output_folder):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output = os.path.join(output_folder, f"{filename}.xlsx")

    doc = pymupdf.open(pdf_path)
    data = []

    for i, page in enumerate(doc):
        data.append({ "Page": i + 1, "Text": page.get_text()})

    df = pd.DataFrame(data)
    df.to_excel(output, index=False)

    doc.close()

# PDF to DOCX
def pdf_to_docx(pdf_path, output_folder):
    filename = os.path.splitext(os.path.basename(pdf_path))
    output = os.path.join(output_folder,f"{filename}.docx")

    cv = Converter(pdf_path)
    try:
        cv.convert(output)
    finally:
        cv.close()

# PDF to JPG
def pdf_to_jpg(pdf_path, output_folder):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    doc = pymupdf.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]

        pix = page.get_pixmap()
        output = os.path.join(output_folder,f"{filename}_{page_num+1}.jpg")
        pix.save(output)
    doc.close()

# PDF to PNG
def pdf_to_png(pdf_path, output_folder):
    filename = os.path.splitext(os.path.basename(pdf_path))
    doc = pymupdf.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]

        pix = page.get_pixmap()
        output = os.path.join(output_folder,f"{filename}_{page_num+1}.jpg")
        pix.save(output)
    doc.close()