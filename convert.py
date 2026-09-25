from pdf2docx import Converter
from PIL import Image

import pandas as pd
import os
import pymupdf

# PDF to TXT
def pdf_to_txt(pdf_path, output_folder):
    pdf = pymupdf.open(pdf_path)
    text = ""

    for page in pdf:
        text += page.get_text()

    filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
    output = os.path.join(output_folder, f"{filename}.txt"),
    with open(output, "w", encoding="utf-8") as f:
        f.write(text)

# PDF to XLSX
def pdf_to_xlsx(pdf_path, output_folder):
    pdf = pymupdf.open(pdf_path)
    text = ""

    for page in pdf:
        text += page.get_text()

    rows = text.splitlines()
    df = pd.DataFrame(rows, columns=["Text"])

    filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".xlsx"
    output = os.path.join(output_folder, f"{filename}.xlsx")
    df.to_excel(output, index=False)

# PDF to DOCX
def pdf_to_docx(pdf_path, output_folder):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output = os.path.join(output_folder,f"{filename}.docx")

    cv = Converter(pdf_path)

    try:
        cv.convert(output)
    finally:
        cv.close()

# PDF to JPG
def pdf_to_jpg(pdf_path, output_folder):
    pdf = pymupdf.open(pdf_path)
    text = ""

    for page in pdf:
        text = page.get_text()

    filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".jpg"
    output = os.path.join(output_folder, f"{filename}.jpg")
    with open(output, "w", encoding="utf-8") as f:
        f.write(text)

# PDF to PNG
def pdf_to_png(pdf_path, output_folder):
    pdf = pymupdf.open(pdf_path)
    text = ""

    for page in pdf:
        text = page.get_text()

    filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".png"
    output = os.path.join(output_folder, f"{filename}.png")
    with open(output, "w", encoding="utf-8") as f:
        f.write(text)