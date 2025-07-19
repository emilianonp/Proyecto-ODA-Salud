# Proyecto ODA Salud

El propósito de este proyecto es centralizar y organizar toda la documentación médica (pagos, consultas, exámenes, recetas, etc.) y ofrecer una interfaz de consulta inteligente para responder preguntas sobre dichos documentos.

## Estructura del proyecto

```
Proyecto-ODA-Salud/
├── data/                     # Documentos originales
│   ├── consultas/
│   ├── examenes/
│   ├── pagos/
│   └── recetas/
├── ingestion/                # Scripts de ingestión y extracción de texto
│   ├── extract_pdf.py
│   ├── ocr_image.py
│   ├── parse_xlsx.py
│   └── processed/
├── index/                    # Construcción del vector store
│   └── build_index.py
├── api/                      # Backend y motor de Q&A
│   ├── main.py
│   └── qa_engine.py
├── ui/                       # Interfaz de usuario
│   └── app.py
├── models/
│   └── config.yaml
├── metadata.db               # Base de datos de metadatos (SQLite)
├── requirements.txt
└── README.md
```

## Uso rápido

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Extraer texto de documentos:
   ```bash
   python ingestion/extract_pdf.py
   python ingestion/ocr_image.py
   python ingestion/parse_xlsx.py
   ```
3. Construir el índice vectorial:
   ```bash
   python index/build_index.py
   ```
4. Levantar la API:
   ```bash
   uvicorn api.main:app --reload
   ```
5. Abrir la interfaz:
   ```bash
   streamlit run ui/app.py
   ```

Con esta arquitectura modular podrás cargar, procesar y consultar tu documentación médica de forma sencilla.
