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
        return {"segments": results}

    except Exception as e:
        print("❌ ERRO no endpoint /diarize:", str(e))
        raise HTTPException(status_code=500, detail=f"Erro ao processar áudio: {e}")
