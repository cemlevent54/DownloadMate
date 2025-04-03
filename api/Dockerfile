FROM python:3.11-slim

# Gerekli sistem paketlerini kur
RUN apt-get update && apt-get install -y ffmpeg unzip && apt-get clean

# Çalışma dizinini ayarla
WORKDIR /app

# requirements.txt'i kopyala ve bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm proje dosyalarını kopyala
COPY . .

# FFmpeg'i belirli dizine kopyala (MoviePy veya senin servis için)
RUN mkdir -p /app/app/setup/FFmpeg/bin \
    && cp $(which ffmpeg) /app/app/setup/FFmpeg/bin/ffmpeg \
    && chmod +x /app/app/setup/FFmpeg/bin/ffmpeg

# Uygulamayı başlat (main.py içindeki "app = FastAPI()")
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]
