# youtubeFiles/info_fetcher.py

import yt_dlp

class InfoFetcher:
    def get_formats(self, url):
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            return {f['format_id']: f"{f['resolution']} - {f['ext']}" for f in formats if 'resolution' in f}

    def get_title(self, url):
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'video')
