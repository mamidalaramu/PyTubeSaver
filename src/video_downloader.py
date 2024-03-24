import threading
from src import gui_handler
from pytube import YouTube

VALID_RESOLUTIONS = ["480p", "720p", "1080p"]
DOWNLOAD_PATH = r""


# set_download_path function
def set_download_path(path):
    global DOWNLOAD_PATH
    DOWNLOAD_PATH = path
    print("Download Path: ", DOWNLOAD_PATH)


# start_download function
def start_download(
    link, finish_label, progress_percentage_label, progress_bar, resolution
):
    try:
        YoutubeLink = link
        youtubeObject = YouTube(
            YoutubeLink,
            on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(
                stream, chunk, bytes_remaining, progress_percentage_label, progress_bar
            ),
        )
        videoDownload = select_resolution(youtubeObject, resolution)
        if videoDownload:
            videoDownload.download(DOWNLOAD_PATH)
            gui_handler.update_download_status("Download Complete", finish_label)
        else:
            raise ValueError("No suitable video stream found.")

    except Exception as e:
        gui_handler.update_download_status(
            "Error while downloading: " + str(e), finish_label
        )


# video_details function
def video_details(
    link,
    finish_label,
    display_title_label,
    display_length_label,
    display_size_label,
    resolution,
):
    try:
        YoutubeLink = link
        video_details = YouTube(YoutubeLink)
        video_title = video_details.title
        length_min = str(video_details.length // 60)
        length_sec = str(video_details.length % 60)
        video_size_mb = get_video_size(video_details, resolution)
        gui_handler.update_display_details(
            video_title,
            length_min,
            length_sec,
            video_size_mb,
            display_title_label,
            display_length_label,
            display_size_label,
        )

    except Exception as e:
        gui_handler.update_download_status(
            "Cannot get video details. : " + str(e), finish_label
        )


# on_progress function
def on_progress(
    stream, chunk, bytes_remaining, progress_percentage_label, progress_bar
):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = int(bytes_downloaded / total_size * 100)
    gui_handler.update_progress_bar(
        percentage_of_completion, progress_percentage_label, progress_bar
    )


# select_resolution function
def select_resolution(youtubeObject, requested_resolution):
    try:
        if requested_resolution and requested_resolution in VALID_RESOLUTIONS:
            videoDownload = youtubeObject.streams.filter(
                res=requested_resolution
            ).first()
            if videoDownload:
                return videoDownload
        # If the requested resolution is not available or not provided, get the highest resolution
        return youtubeObject.streams.get_highest_resolution()

    except Exception as e:
        print(f"Error selecting resolution: {e}")
        return None


# get_video_size function
def get_video_size(video_details, resolution):
    try:
        if resolution:
            video_size = video_details.streams.filter(res=f"{resolution}")
        else:
            video_size = video_details.streams.get_highest_resolution()
        if video_size:
            video_size_bytes = video_size.filesize
            video_size_mb = round(video_size_bytes / (1024 * 1024), 2)
            return f"{video_size_mb} MB"
        else:
            return "Unknown"
    except Exception as e:
        print(f"Error getting video size: {e}")
        return "Unknown"


def get_video_details(
    link,
    finish_label,
    display_title_label,
    display_length_label,
    display_size_label,
    resolution,
):
    threading.Thread(
        target=video_details,
        args=(
            link,
            finish_label,
            display_title_label,
            display_length_label,
            display_size_label,
            resolution,
        ),
    ).start()
