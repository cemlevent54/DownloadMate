import re
import unicodedata

def sanitize_filename(filename):
    """
    Dosya adını geçersiz karakterlerden arındırır ve normalize eder.
    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")  # Emoji ve Unicode'ları sil
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)  # Windows yasaklı karakterleri temizle
    filename = re.sub(r"\s+", "_", filename)  # Boşlukları alt çizgiyle değiştir
    return filename.strip("_")
