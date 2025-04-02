import os
import subprocess
import shutil
import ctypes
import tkinter as tk
from tkinter import messagebox
from elevate import elevate  # elevate modülünü ekliyoruz
import sys

def is_user_admin():
    """
    Kullanıcının yönetici olup olmadığını kontrol eder.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def add_ffmpeg_to_path():
    """
    FFmpeg yolunu sistem PATH ortam değişkenine kalıcı olarak ekler.
    """
    ffmpeg_path = r"C:\ffmpeg\bin"  # FFmpeg'in bulunduğu dizin

    # Windows kayıt defterine PATH eklemek için
    reg_path = r"HKCU\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    
    # Kayıt defterindeki PATH'e ekleme işlemi
    try:
        current_path = os.environ.get('PATH', '')
        if ffmpeg_path not in current_path:
            new_path = f"{current_path};{ffmpeg_path}"
            subprocess.run(
                ["reg", "add", reg_path, "/v", "Path", "/t", "REG_EXPAND_SZ", "/d", new_path, "/f"],
                check=True
            )
            print(f"FFmpeg yolu başarıyla eklenmiştir: {ffmpeg_path}")
        else:
            print("FFmpeg yolu zaten PATH'e eklenmiş.")
    except subprocess.CalledProcessError as e:
        print(f"Yol eklenemedi: {e}")

def ask_for_admin_permission():
    """
    Kullanıcıya yönetici izni olup olmadığını soran MessageBox gösterir.
    """
    root = tk.Tk()
    root.withdraw()  # Pencereyi gizler
    result = messagebox.askyesno(
        "Yönetici İzni Gerekli",
        "Bu işlem için yönetici izni gerekmektedir. Yönetici olarak çalıştırmak ister misiniz?"
    )
    return result

def check_ffmpeg_installed():
    """
    Sistemde FFmpeg'in yüklü olup olmadığını kontrol eder.
    Eğer yüklüyse, yolunu gösterir.
    """
    ffmpeg_path = shutil.which("ffmpeg")  # Sistemdeki ffmpeg'i kontrol et
    if ffmpeg_path:
        print(f"FFmpeg yüklü ve yolu: {ffmpeg_path}")
    else:
        print("FFmpeg yüklü değil, sistem PATH'e eklenmesi gerekiyor.")
        add_ffmpeg_to_path()  # Eğer FFmpeg yüklü değilse, ekleme işlemi yap

def run_as_admin():
    """
    Yönetici olarak tekrar çalıştırmak için Python dosyasını yeniden başlatır.
    """
    if is_user_admin():
        print("Yönetici izinleri alındı.")
        check_ffmpeg_installed()  # FFmpeg'in yüklü olup olmadığını kontrol et
    else:
        # Eğer yönetici değilse, kullanıcıya izin almak için MessageBox göster
        if ask_for_admin_permission():
            print("Yönetici izinleri gerekiyor, yeniden başlatılıyor...")
            # elevate()  # elevate modülü ile yönetici olarak çalıştırma
            check_ffmpeg_installed()  # FFmpeg'in yüklü olup olmadığını kontrol et
        else:
            print("İşlem iptal edildi.")

if __name__ == "__main__":
    if not is_user_admin():
        run_as_admin()  # Yönetici izni alınmaya çalışılıyor
    else:
        check_ffmpeg_installed()  # Yönetici izni alındıktan sonra FFmpeg kontrolü yapılır.
