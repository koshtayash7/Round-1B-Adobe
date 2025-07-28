import fitz  # PyMuPDF
import os

def extract_sections_from_pdfs(input_dir, input_documents):
    section_data = []

    for filename in input_documents:
        pdf_path = os.path.join(input_dir, filename)
        if not os.path.exists(pdf_path):
            print(f"[WARNING] File not found: {pdf_path}")
            continue  # Skip if file does not exist

        doc = fitz.open(pdf_path)
        for page_num, page in enumerate(doc, start=1):
            text_blocks = page.get_text("blocks")
            for block in text_blocks:
                content = block[4].strip()
                if len(content.split()) > 5:  # Skip very short lines
                    section_data.append({
                        "document": filename,
                        "page_number": page_num,
                        "section_title": content[:80],  # First few words as title
                        "text": content
                    })
    return section_data
