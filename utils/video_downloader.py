from yt_dlp import YoutubeDL
from pathlib import Path

def download_video(url, quality, output_folder):
    """
    url: YouTube or Instagram URL
    quality: "360p", "480p", "720p", "1080p"
    output_folder: where to save video
    """
    out_path = Path(output_folder)
    out_path.mkdir(parents=True, exist_ok=True)


    height = quality.replace('p', '')

    ydl_opts = {
        'format': f'bestvideo[height<={height}]+bestaudio/best',
        'outtmpl': str(out_path / '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
