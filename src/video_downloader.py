import logging
from pytube import YouTube, Playlist

VALID_RESOLUTIONS = ["480p", "720p", "1080p"]


def start_download(
    link,
    finish_label,
    progress_percentage_label,
    progress_bar,
    resolution,
    DOWNLOAD_PATH,
):
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
            update_download_status("Download Complete!", finish_label)
        else:
            raise ValueError("No suitable video stream found.")
    except Exception as e:
        update_download_status(f"Error while downloading: {str(e)}", finish_label)
        logging.error(f"Error while downloading: {e}")


def on_progress(
    stream, chunk, bytes_remaining, progress_percentage_label, progress_bar
):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = int(bytes_downloaded / total_size * 100)
    update_progress_bar(
        percentage_of_completion, progress_percentage_label, progress_bar
    )


def select_resolution(youtube_object, requested_resolution):
    try:
        if requested_resolution and requested_resolution in VALID_RESOLUTIONS:
            video_download = youtube_object.streams.filter(
                res=requested_resolution
            ).first()
            if video_download:
                return video_download
        return youtube_object.streams.get_highest_resolution()
    except Exception as e:
        logging.error(f"Error selecting resolution: {e}")
        return None


def download_video_playlist(
    link,
    finish_label,
    progress_percentage_label,
    progress_bar,
    resolution,
    DOWNLOAD_PATH,
):
    try:
        if "&list=" in link or "playlist" in link:
            playlist = Playlist(link)
            for video_links in playlist.video_urls:
                start_download(
                    video_links,
                    finish_label,
                    progress_percentage_label,
                    progress_bar,
                    resolution,
                    DOWNLOAD_PATH,
                )
        else:
            update_download_status("Not a playlist link: ", finish_label)
    except Exception as e:
        print("Error retrieving: ", e)
        update_download_status(f"Error retrieving: {e}", finish_label)


def update_download_status(message, label):
    if message == "Download Complete!":
        text_color = "green"
    else:
        text_color = "red"
    label.configure(text=message, text_color=text_color)


def update_progress_bar(percentage, progress_percentage_label, progress_bar):
    progress_percentage_label.configure(text=f"{percentage}%")
    progress_percentage_label.update()
    progress_bar.set(float(percentage) / 100)
