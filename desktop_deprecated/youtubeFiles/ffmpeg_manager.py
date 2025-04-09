import sys
import os

class FFmpegManager:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        self.ffmpeg_path = os.path.join(base_path, "setup", "FFmpeg", "bin", "ffmpeg.exe")

    def merge(self, video_file, audio_file, output_file):
        if not os.path.exists(self.ffmpeg_path):
            raise FileNotFoundError(f"FFmpeg bulunamadı! Yol: {self.ffmpeg_path}")

        import subprocess
        print("Video ve ses birleştiriliyor...")
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
