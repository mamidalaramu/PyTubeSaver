import threading
import logging
from src import gui_handler
from pytube import YouTube

from src.video_downloader import on_progress

DOWNLOAD_PATH = ""


def start_download_music(
    link,
    finish_label,
    progress_percentage_label,
    progress_bar,
):
    """
    Start downloading the music audio from the provided YouTube link.

    Args:
        link (str): The YouTube video link.
        finish_label: Label to display download status.
        progress_percentage_label: Label to display download progress percentage.
        progress_bar: Progress bar widget to display download progress.
    """
    try:
        youtube_object = YouTube(
            link,
            on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(
                stream, chunk, bytes_remaining, progress_percentage_label, progress_bar
            ),
        )
        music_object = youtube_object.streams.filter(only_audio=True)
        desired_abr = "160kbps"
        music_download = music_object.filter(abr=desired_abr).first()
        if not music_download:
            raise Exception("No audio available")
        else:
            music_download.download(DOWNLOAD_PATH)
            gui_handler.update_download_status("Download Complete!", finish_label)
    except Exception as e:
        gui_handler.update_download_status(f"Error Occurred: {e}", finish_label)
        logging.error(f"Error occurred while downloading music: {e}")
