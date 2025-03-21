from pyannote.audio import Pipeline
from pydub import AudioSegment
import torch
import os
import time

def diarize_speakers(audio_path, output_dir, session_id):
    print("🔍 Loading diarization pipeline...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token="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"
    )

    if torch.cuda.is_available():
        device = torch.device("cuda:0")
        print(f"🚀 Forcing pipeline to use: {torch.cuda.get_device_name(0)}")
        pipeline = pipeline.to(device)
    else:
        print("🧠 No GPU available. Using CPU.")

    audio = AudioSegment.from_file(audio_path)
    duration_sec = len(audio) / 1000
    print(f"📏 Audio duration: {duration_sec:.2f} seconds")

    print(f"🎧 Running diarization on: {audio_path}")

    start_time = time.time()
    diarization = pipeline(audio_path)
    elapsed = time.time() - start_time

    print(f"\n⏱️ Diarization completed in {elapsed:.2f} seconds")
    print(f"⚡ Processing speed: {duration_sec / elapsed:.2f}x real time")

    speaker_path = os.path.join(output_dir, f"speakers-{session_id}.txt")
    with open(speaker_path, "w", encoding="utf-8") as f:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            f.write(f"{turn.start:.2f},{turn.end:.2f},{speaker}\n")

    print(f"👥 Speaker diarization saved to: {speaker_path}")
    return speaker_path
