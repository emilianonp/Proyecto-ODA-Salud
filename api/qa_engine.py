from pathlib import Path
import json
from typing import List, Dict

import faiss
import numpy as np

try:
    import openai
except ImportError:
    raise SystemExit("openai package is required. Install it with pip install openai")

INDEX_PATH = Path('index/faiss.index')
META_PATH = Path('index/meta.json')


def load_index():
    if not INDEX_PATH.exists() or not META_PATH.exists():
        raise FileNotFoundError("Index or metadata not found. Run index/build_index.py first.")
    index = faiss.read_index(str(INDEX_PATH))
    with open(META_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    return index, metadata


def embed_query(query: str):
    resp = openai.Embedding.create(input=query, model='text-embedding-ada-002')
    return np.array(resp['data'][0]['embedding'], dtype='float32')


def buscar_documentos(query: str, k: int = 3) -> List[Dict]:
    index, metadata = load_index()
    query_emb = embed_query(query)
    D, I = index.search(np.array([query_emb]), k)
    results = []
    for idx in I[0]:
        if idx < len(metadata):
            results.append(metadata[idx])
    return results


def generar_respuesta(query: str, docs: List[Dict]) -> str:
    context = "\n\n".join(doc.get("contenido", "")[:1000] for doc in docs)
    prompt = f"Responde la pregunta usando la siguiente informacion:\n{context}\n\nPregunta: {query}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()
