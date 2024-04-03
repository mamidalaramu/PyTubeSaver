import concurrent.futures
from src import gui_handler
from pytube import YouTube


def fetch_details(
    link,
    finish_label,
    display_title_label,
    display_length_label,
    display_size_label,
    resolution,
):
    try:
        youtube_link = link
        video_details = YouTube(youtube_link)
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
            "Cannot get video details: " + str(e), finish_label
        )


def get_video_size(video_details, resolution):
    try:
        if resolution:
            video_size = video_details.streams.filter(res=resolution)
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
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(
            fetch_details,
            link,
            finish_label,
            display_title_label,
            display_length_label,
            display_size_label,
            resolution,
        )
