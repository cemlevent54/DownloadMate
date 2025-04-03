FROM python:3.11-slim

# Gerekli sistem paketlerini kur
RUN apt-get update && apt-get install -y ffmpeg unzip && apt-get clean

# Çalışma dizini
WORKDIR /app

# api klasörü içeriğini kopyala (Dockerfile api içindeyse zaten burası doğru)
COPY . .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# FFmpeg'i doğru dizine kopyala
RUN mkdir -p /app/app/setup/FFmpeg/bin \
    && cp $(which ffmpeg) /app/app/setup/FFmpeg/bin/ffmpeg \
    && chmod +x /app/app/setup/FFmpeg/bin/ffmpeg

# Uygulamayı başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]
