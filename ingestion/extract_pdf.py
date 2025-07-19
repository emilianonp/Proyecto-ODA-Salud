import os
import json
import uuid
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    raise SystemExit("pdfplumber is required. Install it with pip install pdfplumber")

DATA_DIR = Path('data')
OUTPUT_DIR = Path('ingestion/processed')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file using pdfplumber."""
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)


def process_pdfs():
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.lower().endswith('.pdf'):
                path = Path(root) / file
                tipo = Path(root).name  # folder name as type
                content = extract_text_from_pdf(path)
                doc = {
                    "id": uuid.uuid4().hex,
                    "tipo": tipo,
                    "fecha": None,
                    "proveedor": None,
                    "contenido": content,
                    "ruta_archivo": str(path)
                }
                out_file = OUTPUT_DIR / f"{path.stem}.json"
                with open(out_file, 'w', encoding='utf-8') as f:
                    json.dump(doc, f, ensure_ascii=False, indent=2)
                print(f"Processed {path} -> {out_file}")


if __name__ == '__main__':
    process_pdfs()
