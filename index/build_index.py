import json
import os
from pathlib import Path

import faiss
import numpy as np

try:
    import openai
except ImportError:
    raise SystemExit("openai package is required. Install it with pip install openai")

DATA_DIR = Path('ingestion/processed')
INDEX_PATH = Path('index/faiss.index')
META_PATH = Path('index/meta.json')
INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_documents():
    documents = []
    metadata = []
    for file in DATA_DIR.glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            doc = json.load(f)
            documents.append(doc['contenido'])
            metadata.append(doc)
    return documents, metadata


def embed_documents(texts):
    embeddings = []
    for text in texts:
        resp = openai.Embedding.create(input=text, model='text-embedding-ada-002')
        emb = resp['data'][0]['embedding']
        embeddings.append(emb)
    return np.array(embeddings).astype('float32')


def build_index():
    texts, metadata = load_documents()
    if not texts:
        print("No documents found to index.")
        return
    embeddings = embed_documents(texts)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_PATH))
    with open(META_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Index saved to {INDEX_PATH}")


if __name__ == '__main__':
    build_index()
