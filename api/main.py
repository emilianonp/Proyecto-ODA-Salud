from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .qa_engine import buscar_documentos, generar_respuesta

app = FastAPI(title="ODA Salud API")


class QueryRequest(BaseModel):
    question: str


@app.post("/query")
async def query_endpoint(req: QueryRequest):
    try:
        docs = buscar_documentos(req.question)
        answer = generar_respuesta(req.question, docs)
        return {"answer": answer, "documents": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
