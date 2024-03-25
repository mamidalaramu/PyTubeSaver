import threading
import logging
from src import gui_handler
from pytube import YouTube

VALID_RESOLUTIONS = ["480p", "720p", "1080p"]
DOWNLOAD_PATH = r""


# Set download path function
def set_download_path(path):
    """
    Set the download path for the downloaded videos.

    Args:
        path (str): The path where the videos will be downloaded.
    """
    global DOWNLOAD_PATH
    DOWNLOAD_PATH = path
    logging.info(f"Download Path: {DOWNLOAD_PATH}")


# Start download function
def start_download(
    link, finish_label, progress_percentage_label, progress_bar, resolution
):
    """
    Start downloading the video with the provided link.

    Args:
        link (str): The YouTube video link.
        finish_label: Label to display download status.
        progress_percentage_label: Label to display download progress percentage.
        progress_bar: Progress bar widget to display download progress.
        resolution (str): Desired resolution of the video to download.
    """
    try:
        youtube_object = YouTube(
            link,
            on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(
                stream, chunk, bytes_remaining, progress_percentage_label, progress_bar
            ),
        )
        video_download = select_resolution(youtube_object, resolution)
        if video_download:
            video_download.download(DOWNLOAD_PATH)
            gui_handler.update_download_status("Download Complete!", finish_label)
        else:
            raise ValueError("No suitable video stream found.")
    except Exception as e:
        gui_handler.update_download_status(
            f"Error while downloading: {str(e)}", finish_label
        )
        logging.error(f"Error while downloading: {e}")


# On progress function
def on_progress(
    stream, chunk, bytes_remaining, progress_percentage_label, progress_bar
):
    """
    Callback function to update download progress.

    Args:
        stream: The stream being downloaded.
        chunk: The current chunk being downloaded.
        bytes_remaining: Number of bytes remaining to download.
        progress_percentage_label: Label to display download progress percentage.
        progress_bar: Progress bar widget to display download progress.
    """
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = int(bytes_downloaded / total_size * 100)
    gui_handler.update_progress_bar(
        percentage_of_completion, progress_percentage_label, progress_bar
    )


# Select resolution function
def select_resolution(youtube_object, requested_resolution):
    """
    Select the appropriate resolution for the video download.

    Args:
        youtube_object: The YouTube object containing video streams.
        requested_resolution (str): Desired resolution of the video to download.

    Returns:
        The selected video stream.
    """
    try:
        if requested_resolution and requested_resolution in VALID_RESOLUTIONS:
            video_download = youtube_object.streams.filter(
                res=requested_resolution
            ).first()
            if video_download:
                return video_download
        # If the requested resolution is not available or not provided, get the highest resolution
        return youtube_object.streams.get_highest_resolution()
    except Exception as e:
        logging.error(f"Error selecting resolution: {e}")
        return None
