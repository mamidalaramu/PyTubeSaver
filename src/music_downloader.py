import logging
from pytube import YouTube, Playlist
from src.video_downloader import on_progress


def start_download_music(
    link, finish_label, progress_percentage_label, progress_bar, DOWNLOAD_PATH, bitrate
):
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
            update_download_status("No audio available", finish_label)
            raise Exception("No audio available")
        else:
            music_download.download(DOWNLOAD_PATH)
            update_download_status("Download Complete!", finish_label)
    except Exception as e:
        update_download_status(f"Error Occurred: {e}", finish_label)
        logging.error(f"Error occurred while downloading music: {e}")


def download_music_playlist(
    link, finish_label, progress_percentage_label, progress_bar, DOWNLOAD_PATH, bitrate
):
    try:
        if "&list=" in link or "playlist" in link:
            playlist = Playlist(link)
            for audio_link in playlist.video_urls:
                start_download_music(
                    audio_link,
                    finish_label,
                    progress_percentage_label,
                    progress_bar,
                    DOWNLOAD_PATH,
                    bitrate,
                )
        else:
            update_download_status("Not a Playlist link", finish_label)

    except Exception as e:
        print("Exception : ", e)
        update_download_status(f"Error retrieving: {e}", finish_label)


def update_download_status(message, label):
    if message == "Download Complete!":
        text_color = "green"
    else:
        text_color = "red"
    label.configure(text=message, text_color=text_color)
