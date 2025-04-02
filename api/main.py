from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.youtube.downloader import YoutubeDownloadAPI
from app.schemas import YouTubeDownloadRequest  # Sadece YouTubeDownloadRequest'yi import ediyoruz
from fastapi.responses import FileResponse
import os

app = FastAPI()
downloader = YoutubeDownloadAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/youtube")
async def youtube():
    return {"message": "YouTube API endpoint"}

@app.post("/twitter")
async def twitter():
    return {"message": "Twitter API endpoint"}

@app.post("/instagram")
async def instagram():
    return {"message": "Instagram API endpoint"}

@app.post("/sample")
async def sample():
    if True:
        return {"message": "Sample API endpoint"}
    else:
        raise HTTPException(status_code=404, detail="Sample API endpoint failed")

# Tek bir endpoint ile hem ses hem de video indirme
# @app.post("/youtube/download")
# async def youtube_download(request: YouTubeDownloadRequest):
#     try:
#         # Indirme işlemine başla
#         result = downloader.download(request.url, request.type)
        
#         # Başarıyla indirme yapıldıysa döndürülen dosya adı ile birlikte mesaj ver
#         return {"message": f"{request.type.capitalize()} download started", "file_name": f"downloaded_file.{request.type}"}
    
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))  # Geçersiz tür hatası
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")  # Diğer hatalar

@app.post("/youtube/download")
async def youtube_download(request: YouTubeDownloadRequest):
    try:
        # İndirme işlemi başlatılır
        result = downloader.download(request.url, request.type)

        # İndirme işlemi başarıyla tamamlandıysa dosyayı kullanıcıya döndür
        if result:
            if request.type == "audio":
                return FileResponse(result, media_type="audio/mp3", headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"})
            elif request.type == "video":
                return FileResponse(result, media_type="video/mp4", headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"})
            
        raise HTTPException(status_code=500, detail="Video indirilemedi.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

