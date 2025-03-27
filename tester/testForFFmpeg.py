import shutil
import os

def find_ffmpeg():
    """
    FFmpeg'in yüklü olup olmadığını kontrol eder ve yolunu döner.
    """
    # FFmpeg'in sistem PATH'inde olup olmadığını kontrol et
    ffmpeg_path = shutil.which("ffmpeg")
    
    if ffmpeg_path:
        print(f"FFmpeg bulundu: {ffmpeg_path}")
    else:
        print("FFmpeg sistemde bulunamadı.")
    
    return ffmpeg_path

def find_local_ffmpeg():
    """
    FFmpeg'in yerel dizinde olup olmadığını kontrol eder.
    """
    # Yerel dizin içinde FFmpeg'i arar
    current_directory = os.getcwd()
    ffmpeg_local_path = os.path.join(current_directory, 'setup', 'FFmpeg', 'bin', 'ffmpeg.exe')

    if os.path.exists(ffmpeg_local_path):
        print(f"FFmpeg bulundu (yerel dizin): {ffmpeg_local_path}")
    else:
        print("FFmpeg yerel dizinde bulunamadı.")

if __name__ == "__main__":
    find_ffmpeg()  # Sistemdeki FFmpeg'i kontrol et
    find_local_ffmpeg()  # Yerel dizindeki FFmpeg'i kontrol et
