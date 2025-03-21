import os
import uuid
from get_file import download_and_convert_audio
from transcribe import transcribe_and_save
from diarize import diarize_speakers
from combine import combine_speakers_and_transcript

def process_audio(drive_url):
    session_id = str(uuid.uuid4())
    output_dir = os.path.join(os.getcwd(), session_id)
    os.makedirs(output_dir, exist_ok=True)

    print(f"📁 Created session folder: {output_dir}")

    # Step 1: Download and Convert
    mp3_path = download_and_convert_audio(drive_url)
    if not mp3_path:
        print("❌ Failed to download or convert audio.")
        return

    new_mp3_path = os.path.join(output_dir, f"audio-{session_id}.mp3")
    os.rename(mp3_path, new_mp3_path)

    # Step 2: Transcribe
    transcription_json = transcribe_and_save(new_mp3_path, output_dir, session_id)

    # Step 3: Diarize
    speakers_txt = diarize_speakers(new_mp3_path, output_dir, session_id)

    # Step 4: Combine
    combined_output = combine_speakers_and_transcript(transcription_json, speakers_txt, output_dir, session_id)

    print(f"\n✅ All done! Check your folder: {output_dir}")

if __name__ == "__main__":
    drive_link = input("🔗 Enter the Google Drive URL of the audio file: ").strip()
    if drive_link:
        process_audio(drive_link)
    else:
        print("❌ No URL provided. Exiting.")
