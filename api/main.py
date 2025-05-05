from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.youtube.downloader import YoutubeDownloadAPI
from app.schemas import FacebookDownloadRequest, TikTokDownloadRequest, YouTubeDownloadRequest, InstagramDownloadRequest, TwitterDownloadRequest  # Sadece YouTubeDownloadRequest'yi import ediyoruz
from app.instagram.downloader import InstagramDownloadAPI
from app.twitter.downloader import TwitterDownloadAPI
from app.tiktok.downloader import TiktokDownloadAPI
from app.facebook.downloader import FacebookDownloadAPI
from fastapi.responses import FileResponse
import os
from fastapi.logger import logger
import traceback2 as traceback
from fastapi import Request  # <--- request nesnesini alabilmek için


app = FastAPI()

app = FastAPI(
    title="Downloader API",
    description="API to download media from various platforms.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


downloader = YoutubeDownloadAPI()
instagram_downloader = InstagramDownloadAPI()
twitter_downloader = TwitterDownloadAPI()
tiktok_downloader = TiktokDownloadAPI()
facebook_downloader = FacebookDownloadAPI()
@app.get("/")
def root():
    return {"message": "API is workings ✅"}

@app.post("/sample")
async def sample():
    if True:
        return {"message": "Sample API endpoint"}
    else:
        raise HTTPException(status_code=404, detail="Sample API endpoint failed")

# YouTube indirme isteği için endpoint
@app.post("/youtube/download")
async def youtube_download(request: YouTubeDownloadRequest, fastapi_request: Request):
    try:
        logger.info(f"[▶️] YouTube indirme isteği alındı: URL={request.url}, TYPE={request.type}")

        # 🍪 Mobilden gelen Cookie'yi al
        cookies = fastapi_request.headers.get("cookie")
        if cookies:
            logger.info("[🍪] Cookie bulundu, gönderiliyor...")
        else:
            logger.warning("[❌] Cookie header'ı bulunamadı")
            raise HTTPException(status_code=401, detail="Lütfen önce giriş yaparak çerez alın.")

        # ⏬ Çerezle birlikte indirme başlat
        result = downloader.download(request.url, request.type, cookies=cookies)

        if result:
            logger.info(f"[✅] YouTube indirme başarılı. Dosya: {result}")
            media_type = "audio/mp3" if request.type == "audio" else "video/mp4"
            return FileResponse(
                result,
                media_type=media_type,
                headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"}
            )

        logger.warning("[⚠️] Dosya döndürülemedi. Result None döndü.")
        raise HTTPException(status_code=500, detail="Video indirilemedi.")

    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error(f"[🔥] YouTube indirme hatası: {e}\n{error_trace}")
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")
    

# instagram indirme isteği için endpoint
@app.post("/instagram/download")
async def instagram_download(request: InstagramDownloadRequest, fastapi_request: Request):
    try:
        logger.info(f"[▶️] Instagram indirme isteği alındı: URL={request.url}, TYPE={request.type}")

        # 🍪 Header'lardan Cookie al
        cookies = fastapi_request.headers.get("cookie")
        if cookies:
            logger.info(f"[🍪] Cookie bulundu, gönderiliyor...")
        else:
            logger.warning("[❌] Cookie header'ı bulunamadı")
            raise HTTPException(status_code=401, detail="Lütfen önce giriş yaparak çerez alın.")

        # ⏬ İndirme işlemi (cookie parametresi ile)
        result = instagram_downloader.download(request.url, request.type, cookies=cookies)

        # ✅ Başarılıysa dosyayı döndür
        if result:
            logger.info(f"[✅] Instagram indirme başarılı. Dosya: {result}")
            media_type = "audio/mp3" if request.type == "audio" else "video/mp4"
            return FileResponse(
                result,
                media_type=media_type,
                headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"}
            )

        logger.warning("[⚠️] Instagram dosya döndürülemedi. Result None döndü.")
        raise HTTPException(status_code=500, detail="Instagram videosu indirilemedi.")

    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error(f"[🔥] Instagram indirme hatası: {e}\n{error_trace}")
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")


    
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
    
@app.post("/tiktok/download")
async def tiktok_download(request: TikTokDownloadRequest):
    try:
        # İndirme işlemi başlatılır
        result = tiktok_downloader.download(request.url, request.type)

        # İndirme işlemi başarıyla tamamlandıysa dosyayı kullanıcıya döndür
        if result:
            if request.type == "audio":
                return FileResponse(result, media_type="audio/mp3", headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"})
            elif request.type == "video":
                return FileResponse(result, media_type="video/mp4", headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"})
        
        raise HTTPException(status_code=500, detail="Video indirilemedi.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/facebook/download")
async def facebook_download(request: FacebookDownloadRequest):
    try:
        # İndirme işlemi başlatılır
        result = facebook_downloader.download(request.url, request.type)

        # İndirme işlemi başarıyla tamamlandıysa dosyayı kullanıcıya döndür
        if result:
            if request.type == "audio":
                return FileResponse(result, media_type="audio/mp3", headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"})
            elif request.type == "video":
                return FileResponse(result, media_type="video/mp4", headers={"Content-Disposition": f"attachment; filename={os.path.basename(result)}"})
        
        raise HTTPException(status_code=500, detail="Video indirilemedi.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8010))  # Railway dinamik port verir
    uvicorn.run("main:app", host="0.0.0.0", port=port)