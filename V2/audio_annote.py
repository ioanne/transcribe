from pyannote.audio import Pipeline
import os
import uuid

def diarize_speakers(audio_path):
    # Cargar pipeline de diarización
    print("🔍 Loading diarization pipeline...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token='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'
    )

    print(f"🎧 Processing audio: {audio_path}")
    diarization = pipeline(audio_path)

    # Crear carpeta para resultados
    session_id = str(uuid.uuid4())
    output_dir = os.path.join(os.getcwd(), session_id)
    os.makedirs(output_dir, exist_ok=True)
    txt_path = os.path.join(output_dir, "speakers.txt")

    # Guardar resultados
    with open(txt_path, "w", encoding="utf-8") as f:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            line = f"[{turn.start:.2f}s - {turn.end:.2f}s] {speaker}\n"
            print(line.strip())
            f.write(line)

    print(f"✅ Diarization result saved at: {txt_path}")
    return txt_path
