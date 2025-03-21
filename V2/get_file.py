import gdown
from pydub import AudioSegment
import os
import time

def download_and_convert_audio(drive_url):
    file_id = None
    if "/file/d/" in drive_url:
        file_id = drive_url.split("/file/d/")[1].split("/")[0]
    elif "id=" in drive_url:
        file_id = drive_url.split("id=")[-1].split("&")[0]

    if not file_id:
        print("❌ Could not extract file ID from the URL.")
        return None

    real_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    output_name = "downloaded_file.mp4"

    print("Downloading file...")
    gdown.download(real_url, output_name, quiet=False, fuzzy=True)

    timeout = 360
    elapsed = 0
    while (not os.path.exists(output_name) or os.path.getsize(output_name) < 1024 * 1024) and elapsed < timeout:
        print("⌛ Waiting for complete download...")
        time.sleep(2)
        elapsed += 2

    if os.path.getsize(output_name) < 1024 * 1024:
        print("❌ Downloaded file is incomplete.")
        return None

    print("Detecting audio format...")
    try:
        audio = AudioSegment.from_file(output_name)
        mp3_filename = "converted_audio.mp3"
        audio.export(mp3_filename, format="mp3")
        print(f"✅ Converted audio saved as: {mp3_filename}")
        os.remove(output_name)
        return mp3_filename
    except Exception as e:
        print(f"❌ Error converting the file: {e}")
        return None
