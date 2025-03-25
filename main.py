from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pyannote.audio import Pipeline
import tempfile
import shutil
import os

# ✅ Primeiro, crie a instância do app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variável global para o pipeline

pipeline = None
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

if not HUGGINGFACE_TOKEN:
    raise RuntimeError("HUGGINGFACE_TOKEN não está definido nas variáveis de ambiente!")

try:
    print("🔁 Carregando modelo do Hugging Face...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=HUGGINGFACE_TOKEN
    )
    print("✅ Modelo carregado com sucesso.")
except Exception as e:
    raise RuntimeError(f"Erro ao carregar pipeline: {e}")

# ✅ Só agora defina os endpoints da API
@app.post("/diarize")
async def diarize_audio(file: UploadFile = File(...)):
    try:
        print("⏳ Iniciando processamento do arquivo...")

        if pipeline is None:
            raise HTTPException(status_code=500, detail="Pipeline não está carregado")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        print(f"✅ Arquivo salvo temporariamente em: {tmp_path}")
        print("🎧 Enviando arquivo para o pipeline...")

        diarization = pipeline(tmp_path)

        print("✅ Diarização concluída com sucesso!")

        results = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            results.append({
                "speaker": speaker,
                "start": round(turn.start, 2),
                "end": round(turn.end, 2)
            })

        print(f"📦 Retornando {len(results)} segmentos")
        return {"segments": results"}

    except Exception as e:  # ✅ Alinhado com try
        import traceback
        print("❌ ERRO no endpoint /diarize:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao processar áudio: {e}")


