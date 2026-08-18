import os
import shutil
import sys


async def download_and_extract_ffmpeg(bot, target_dir=None):
    """Returns path to ffmpeg. In containers, uses system-installed Linux ffmpeg.
    On macOS dev, uses the bundled macOS binary and downloads it if missing."""

    # In containers (Docker), use the apt-installed Linux ffmpeg on PATH.
    if os.path.exists('/.dockerenv'):
        from print_color import print
        system_ffmpeg = shutil.which('ffmpeg')
        if system_ffmpeg:
            print(f"FFmpeg found at {system_ffmpeg}", tag_color='green', tag="SUCCESS", color='white')
            return system_ffmpeg
        print("FFmpeg not found on PATH inside container.", tag_color='red', tag="ERROR", color='white')
        return 'ffmpeg'

    if target_dir is None:
        target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'executables')

    ffmpeg_path = os.path.join(target_dir, 'ffmpeg')

    # If the bundled macOS ffmpeg already exists, return it
    if os.path.exists(ffmpeg_path) and os.path.getsize(ffmpeg_path) > 1000000:  # > 1MB
        from print_color import print
        print(f"FFmpeg found at {ffmpeg_path}", tag_color='green', tag="SUCCESS", color='white')
        return ffmpeg_path

    # On macOS dev, download if missing
    from print_color import print
    import requests

    print("\nDownloading and Extracting FFMPEG...")
    os.makedirs(target_dir, exist_ok=True)

    download_url = "https://evermeet.cx/ffmpeg/getrelease/zip"
    try:
        response = requests.get(download_url, stream=True, timeout=30)
        response.raise_for_status()

        filename = os.path.join(target_dir, os.path.basename(download_url))
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        import zipfile
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(target_dir)

        os.remove(filename)
        print("FFmpeg downloaded and extracted successfully.", tag_color='green', tag="SUCCESS", color='white')
    except Exception as e:
        print(f"Failed to download FFmpeg: {e}", tag_color='red', tag="ERROR", color='white')

    return ffmpeg_path
