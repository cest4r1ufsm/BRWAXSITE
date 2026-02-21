import fitz
import json

pdf_path = "Cópia de brwaxx_2024.pdf"
doc = fitz.open(pdf_path)

extracted_text = []

for page_num, page in enumerate(doc):
    text = page.get_text("text")
    extracted_text.append(f"--- Page {page_num + 1} ---\n{text}\n")

with open("pdf_content_dump.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(extracted_text))

print("PDF content dumped to pdf_content_dump.txt")
