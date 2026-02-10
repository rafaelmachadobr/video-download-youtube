import yt_dlp

class YTDLPService:
    def download(self, url: str):
        ydl_opts = {
            "outtmpl": "downloads/%(title)s.%(ext)s"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title")
            filename = ydl.prepare_filename(info)

        return title, filename
