from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pyannote.audio import Pipeline
import tempfile
import shutil
import subprocess
import os

# Cria a instância do FastAPI
app = FastAPI()

# Libera CORS (pode ajustar para domínios específicos se quiser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Token da Hugging Face
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

if not HUGGINGFACE_TOKEN:
    raise RuntimeError("❌ HUGGINGFACE_TOKEN não está definido!")

# Carrega o pipeline do pyannote
print("🔁 Carregando modelo do Hugging Face...")
try:
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=HUGGINGFACE_TOKEN
    )
    print("✅ Modelo carregado com sucesso.")
except Exception as e:
    raise RuntimeError(f"Erro ao carregar pipeline: {e}")

# Função auxiliar: converte qualquer áudio para WAV válido
def convert_to_wav(input_path: str) -> str:
    output_path = input_path.replace(".wav", "_converted.wav")
    try:
        subprocess.run([
            "ffmpeg",
            "-i", input_path,
            "-ar", "16000",  # taxa de amostragem
            "-ac", "1",      # mono
            "-y",            # sobrescreve
            output_path
        ], check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro ao converter áudio para WAV: {e}")

@app.post("/diarize")
async def diarize_audio(file: UploadFile = File(...)):
    try:
        print("⏳ Iniciando processamento do arquivo...")

        if pipeline is None:
            raise HTTPException(status_code=500, detail="Pipeline não está carregado")

        # Salva temporariamente o arquivo original
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        print(f"📁 Arquivo salvo em: {tmp_path}")

        # Converte para WAV válido (mono, 16kHz)
        wav_path = convert_to_wav(tmp_path)
        print(f"🎙️ Arquivo convertido para: {wav_path}")

        # Roda a diarização
        print("🔍 Executando diarização...")
        diarization = pipeline(wav_path)
        print("✅ Diarização concluída.")

        # Extrai os segmentos
        results = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            results.append({
                "speaker": speaker,
                "start": round(turn.start, 2),
                "end": round(turn.end, 2)
            })

        print(f"📦 Retornando {len(results)} segmentos.")
        return {"segments": results}

    except Exception as e:
        import traceback
        print("❌ ERRO no endpoint /diarize:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao processar áudio: {e}")
