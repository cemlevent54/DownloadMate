FROM python:3.11-slim

# Sistem bağımlılıklarını yükle (FFmpeg dahil)
RUN apt-get update && apt-get install -y ffmpeg unzip && apt-get clean

# Uygulama dizini
WORKDIR /app

# requirements.txt dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Tüm proje dosyalarını kopyala (app/, main.py vs.)
COPY . .

# FFmpeg'i proje içindeki özel klasöre kopyala (MoviePy veya özel kullanım için)
RUN mkdir -p /app/app/setup/FFmpeg/bin \
    && cp $(which ffmpeg) /app/app/setup/FFmpeg/bin/ffmpeg \
    && chmod +x /app/app/setup/FFmpeg/bin/ffmpeg

# Uvicorn ile FastAPI uygulamasını başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]
