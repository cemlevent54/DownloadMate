# youtubeFiles/ffmpeg_manager.py

import os
import subprocess

class FFmpegManager:
    def __init__(self):
        self.ffmpeg_path = os.path.join(os.getcwd(), "setup", "ffmpeg", "bin", "ffmpeg.exe")

    def merge(self, video_file, audio_file, output_file):
        print("Video ve ses birleştiriliyor...")
        try:
            subprocess.run([
                self.ffmpeg_path,
                '-i', video_file,
                '-i', audio_file,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest',
                '-y',
                '-loglevel', 'error',
                output_file
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Birleştirme hatası: {e}")
