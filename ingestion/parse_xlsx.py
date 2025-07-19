import os
import json
import uuid
from pathlib import Path

try:
    import openpyxl
except ImportError:
    raise SystemExit("openpyxl is required. Install it with pip install openpyxl")

DATA_DIR = Path('data')
OUTPUT_DIR = Path('ingestion/processed')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def process_xlsx():
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.lower().endswith('.xlsx'):
                path = Path(root) / file
                tipo = Path(root).name
                wb = openpyxl.load_workbook(path, data_only=True)
                text_parts = []
                for sheet in wb.worksheets:
                    for row in sheet.iter_rows(values_only=True):
                        line = ' '.join(str(cell) for cell in row if cell is not None)
                        if line:
                            text_parts.append(line)
                content = '\n'.join(text_parts)
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
    process_xlsx()
