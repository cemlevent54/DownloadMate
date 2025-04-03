from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.youtube.downloader import YoutubeDownloadAPI
from app.schemas import YouTubeDownloadRequest, InstagramDownloadRequest, TwitterDownloadRequest  # Sadece YouTubeDownloadRequest'yi import ediyoruz
from app.instagram.downloader import InstagramDownloadAPI
from app.twitter.downloader import TwitterDownloadAPI
from fastapi.responses import FileResponse
import os


app = FastAPI()
downloader = YoutubeDownloadAPI()
instagram_downloader = InstagramDownloadAPI()
twitter_downloader = TwitterDownloadAPI()
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

# YouTube indirme isteği için endpoint
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
    

# instagram indirme isteği için endpoint
@app.post("/instagram/download")
async def instagram_download(request: InstagramDownloadRequest):
    try:
        # İndirme işlemi başlatılır
        result = instagram_downloader.download(request.url, request.type)

        # İndirme işlemi başarıyla tamamlandıysa dosyayı kullanıcıya döndür
        if result:
            if request.type == "audio":
                return FileResponse(result, media_type="audio/mp3", headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"})
            elif request.type == "video":
                return FileResponse(result, media_type="video/mp4", headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"})
        
        raise HTTPException(status_code=500, detail="Video indirilemedi.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Twitter indirme isteği için endpoint
@app.post("/twitter/download")
async def twitter_download(request: TwitterDownloadRequest):
    try:
        # İndirme işlemi başlatılır
        result = twitter_downloader.download(request.url, request.type)

        # İndirme işlemi başarıyla tamamlandıysa dosyayı kullanıcıya döndür
        if result:
            if request.type == "audio":
                return FileResponse(result, media_type="audio/mp3", headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"})
            elif request.type == "video":
                return FileResponse(result, media_type="video/mp4", headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"})
        
        raise HTTPException(status_code=500, detail="Video indirilemedi.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))