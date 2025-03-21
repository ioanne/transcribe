import json
import os

def load_speakers(speaker_file):
    speakers = []
    with open(speaker_file, "r", encoding="utf-8") as f:
        for line in f:
            start, end, speaker = line.strip().split(",")
            speakers.append({
                "start": float(start),
                "end": float(end),
                "speaker": speaker
            })
    return speakers

def find_speaker_for_segment(segment, speakers):
    max_overlap = 0
    matched_speaker = "UNKNOWN"
    
    for s in speakers:
        overlap_start = max(segment["start"], s["start"])
        overlap_end = min(segment["end"], s["end"])
        overlap = max(0.0, overlap_end - overlap_start)

        if overlap > max_overlap:
            max_overlap = overlap
            matched_speaker = s["speaker"]

    return matched_speaker


def combine_speakers_and_transcript(transcript_json, speaker_txt, output_dir, session_id):
    with open(transcript_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    speakers = load_speakers(speaker_txt)

    output_path = os.path.join(output_dir, f"combined-{session_id}.txt")
    with open(output_path, "w", encoding="utf-8") as out:
        for segment in data["segments"]:
            speaker = find_speaker_for_segment(segment, speakers)
            out.write(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {speaker}: {segment['text']}\n")

    print(f"🧩 Combined transcription saved to: {output_path}")
    return output_path
