import whisper
import os
import json

def transcribe_and_save(mp3_path, output_dir, session_id):
    print("⏳ Loading Whisper model...")
    model = whisper.load_model("medium")

    print(f"🎧 Transcribing {mp3_path}...")
    result = model.transcribe(mp3_path, language="es", verbose=False)

    txt_path = os.path.join(output_dir, f"transcription-{session_id}.txt")
    json_path = os.path.join(output_dir, f"transcription-{session_id}.json")

    with open(txt_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            f.write(segment["text"] + " ")
            f.flush()

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(result, jf, ensure_ascii=False, indent=2)

    print(f"📝 Saved transcription to {txt_path}")
    return json_path
