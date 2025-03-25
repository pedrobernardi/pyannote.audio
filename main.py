from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pyannote.audio import Pipeline
import tempfile
import shutil
import os

app = FastAPI()

# CORS liberado para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa pipeline em nível global
pipeline = None
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

if not HUGGINGFACE_TOKEN:
    raise RuntimeError("HUGGINGFACE_TOKEN não está definido nas variáveis de ambiente!")

try:
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=HUGGINGFACE_TOKEN
    )
except Exception as e:
    raise RuntimeError(f"Erro ao carregar pipeline: {e}")

@app.post("/diarize")
async def diarize_audio(file: UploadFile = File(...)):
    if pipeline is None:
        raise HTTPException(status_code=500, detail="Pipeline não está carregado")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        diarization = pipeline(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a diarização: {e}")

    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        results.append({
            "speaker": speaker,
            "start": round(turn.start, 2),
            "end": round(turn.end, 2)
        })

    return {"segments": results}
