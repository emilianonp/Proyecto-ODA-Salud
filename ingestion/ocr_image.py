import os
import json
import uuid
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow is required. Install it with pip install pillow")

try:
    import pytesseract
except ImportError:
    raise SystemExit("pytesseract is required. Install it with pip install pytesseract")

DATA_DIR = Path('data')
OUTPUT_DIR = Path('ingestion/processed')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_text_from_image(image_path: Path) -> str:
    """Use Tesseract OCR to extract text from an image file."""
    return pytesseract.image_to_string(Image.open(image_path))


def process_images():
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):
                path = Path(root) / file
                tipo = Path(root).name
                content = extract_text_from_image(path)
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
    process_images()
