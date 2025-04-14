import fitz  # PyMuPDF
from pathlib import Path

def extract_pdf_chunks(pdf_path: Path, max_chunk_size=800):
    doc = fitz.open(pdf_path)
    chunks = []
    for page_num, page in enumerate(doc, 1):
        text = page.get_text()
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        for para in paragraphs:
            if len(para) > max_chunk_size:
                # further split by sentences if needed
                sentences = para.split('. ')
                chunk = ""
                for s in sentences:
                    if len(chunk + s) < max_chunk_size:
                        chunk += s + ". "
                    else:
                        chunks.append((f"p{page_num}", chunk.strip()))
                        chunk = s + ". "
                if chunk:
                    chunks.append((f"p{page_num}", chunk.strip()))
            else:
                chunks.append((f"p{page_num}", para))
    return chunks
