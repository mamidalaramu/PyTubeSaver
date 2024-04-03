import tkinter as tk
import customtkinter as ctk
from src import video_downloader, music_downloader, get_details, settings
from concurrent.futures import ThreadPoolExecutor

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("src/themes/SweetKind.json")


class DownloaderApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("PyTubeSaver")
        self.app.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.create_heading()
        self.create_input_url_frame()
        self.create_download_path_format_frame()
        self.create_resolution_bitrate_widgets()
        self.create_link_details_frame()
        self.create_download_button()
        self.create_progress_widgets()

    def create_heading(self):
        heading = ctk.CTkLabel(self.app, text="PyTubeSaver", font=("Arial", 32, "bold"))
        heading.pack(pady=20)

    def create_input_url_frame(self):
        input_url_frame = ctk.CTkFrame(self.app)
        input_url_frame.pack()

        title = ctk.CTkLabel(
            input_url_frame,
            text="Insert a link to download",
            font=("Arial", 18, "bold"),
        )
        title.pack(side="top", padx=10)

        self.url_var = tk.StringVar()
        self.link_entry = ctk.CTkEntry(
            input_url_frame, width=550, height=40, textvariable=self.url_var
        )
        self.link_entry.pack(side="left", padx=20, pady=10)

    def create_download_path_format_frame(self):
        download_path_format_frame = ctk.CTkFrame(self.app)
        download_path_format_frame.pack(pady=(10, 0))

        download_path_label = ctk.CTkLabel(
            download_path_format_frame, text="Download Path:"
        )
        download_path_label.pack(side="left", padx=20)

        self.path_entry = ctk.CTkEntry(download_path_format_frame, width=200)
        self.path_entry.pack(side="left")

        self.format_var = tk.StringVar()
        self.format_var.set("Video")

        self.format_dropdown = ctk.CTkOptionMenu(
            download_path_format_frame,
            values=[
                "Video",
                "MP3",
                "Playlist Video",
                "Playlist Audio",
            ],
            variable=self.format_var,
        )

        self.format_dropdown.pack(side="left", padx=10)

        self.resolution_entry = ctk.CTkEntry(
            download_path_format_frame, placeholder_text="resolution"
        )
        self.resolution_entry.pack(side="left", padx=10)

        self.bitrate_entry = ctk.CTkEntry(
            download_path_format_frame, placeholder_text="bitrate"
        )
        self.bitrate_entry.pack(side="left", padx=10)

    def create_resolution_bitrate_widgets(self):
        pass

    def create_link_details_frame(self):
        link_details_frame = ctk.CTkFrame(self.app)
        link_details_frame.pack(pady=(10, 0))

        self.video_details = ctk.CTkLabel(
            link_details_frame,
            text="Video Details: ",
            font=("Roboto", 16, "bold"),
        )
        self.video_details.pack(padx="10", pady=(20, 0))

        self.title_label = ctk.CTkLabel(link_details_frame, text="")
        self.title_label.pack(padx="10", pady="10")

        self.length_label = ctk.CTkLabel(link_details_frame, text="")
        self.length_label.pack(padx="10")

        self.size_label = ctk.CTkLabel(link_details_frame, text="")
        self.size_label.pack(padx="10")

    def create_download_button(self):
        self.download_button = ctk.CTkButton(
            self.app, text="DOWNLOAD", command=self.start_download
        )
        self.download_button.pack(pady=10)

    def create_progress_widgets(self):
        self.finish_label = ctk.CTkLabel(self.app, text="")
        self.finish_label.pack()

        self.progress_percentage_label = ctk.CTkLabel(self.app, text="0%")
        self.progress_percentage_label.pack()

        self.progress_bar = ctk.CTkProgressBar(self.app, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=10, pady=10)

    def start_download(self):

        youtube_link = self.link_entry.get()
        download_path = self.path_entry.get()
        download_format = self.format_var.get()
        resolution = self.resolution_entry.get() or None
        bitrate = self.bitrate_entry.get() or None

        if not youtube_link:
            self.finish_label.configure(
                text="Link cannot be empty",
                text_color="red",
                font=("Arial", 16, "bold"),
            )
            return
        self.finish_label.configure(text="")
        download_path = settings.DOWNLOAD_PATH if settings.DOWNLOAD_PATH else None

        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(
            self.download_async,
            youtube_link,
            download_path,
            download_format,
            resolution,
            bitrate,
        )

    def download_async(
        self, youtube_link, download_path, download_format, resolution, bitrate
    ):
        try:
            get_details.fetch_details(
                youtube_link,
                self.finish_label,
                self.title_label,
                self.length_label,
                self.size_label,
                (
                    resolution
                    if download_format != "MP3" and download_format != "Playlist Audio"
                    else None
                ),
            )

            download_functions = {
                "Video": video_downloader.start_download,
                "MP3": music_downloader.start_download_music,
                "Playlist Video": video_downloader.download_video_playlist,
                "Playlist Audio": music_downloader.download_music_playlist,
            }

            download_function = download_functions.get(download_format)
            if download_function:
                if download_format == "MP3" or download_format == "Playlist Audio":

                    download_function(
                        youtube_link,
                        self.finish_label,
                        self.progress_percentage_label,
                        self.progress_bar,
                        download_path,
                        bitrate,
                    )
                else:
                    download_function(
                        youtube_link,
                        self.finish_label,
                        self.progress_percentage_label,
                        self.progress_bar,
                        resolution,
                        download_path,
                    )
            else:
                raise ValueError(f"Invalid download format: {download_format}")
        except Exception as e:
            self.finish_label.configure(
                text=f"Error occurred: {str(e)}",
                text_color="red",
                font=("Arial", 16, "bold"),
            )


if __name__ == "__main__":
    app_instance = DownloaderApp()
    app_instance.app.mainloop()
