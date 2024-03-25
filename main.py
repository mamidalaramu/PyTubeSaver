import tkinter as tk
import customtkinter as ctk
from src import video_downloader, music_downloader, get_details
import threading


class DownloaderApp:
    def __init__(self):
        self.app = ctk.CTk()
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")
        self.app.geometry("800x600")
        self.app.title("PyTubeSaver")
        self.create_widgets()

    def create_widgets(self):
        # Heading
        heading = ctk.CTkLabel(
            self.app, text="PyTubeSaver", font=("Roboto", 32, "bold")
        )
        heading.pack(pady=20)

        # Download path frame
        path_frame = ctk.CTkFrame(self.app)
        path_frame.pack()

        path_label = ctk.CTkLabel(path_frame, text="Download Path: ")
        path_label.pack(side="left", padx="20")

        self.path_entry = ctk.CTkEntry(path_frame, width=200)
        self.path_entry.pack(side="left")

        # path save button
        path_save_button = ctk.CTkButton(
            self.app, text="Save path", command=self.save_download_path
        )
        path_save_button.pack(padx=10, pady=(20, 0))

        # title label
        title = ctk.CTkLabel(
            self.app,
            text="Insert a youtube video link to download",
            font=("Roboto", 18, "bold"),
        )
        title.pack(padx=10, pady=10)

        input_url_frame = ctk.CTkFrame(self.app)
        input_url_frame.pack()

        self.url_var = tk.StringVar()
        self.link = ctk.CTkEntry(
            input_url_frame,
            width=350,
            height=30,
            placeholder_text="Video url",
            placeholder_text_color="white",
            textvariable=self.url_var,
        )
        self.link.pack(side="left", padx="20")

        resolution_lable = ctk.CTkLabel(input_url_frame, text="Resolution: ")
        resolution_lable.pack(side="left", padx="10")

        self.res_value = tk.StringVar()
        self.resolution_input = ctk.CTkEntry(
            input_url_frame, width=40, height=30, textvariable=self.res_value
        )
        self.resolution_input.pack(side="left")

        # Video details labels
        self.video_details = ctk.CTkLabel(self.app, text="Video Details: ")
        self.video_details.pack(padx="10", pady="10")

        self.display_title_label = ctk.CTkLabel(self.app, text="")
        self.display_title_label.pack(padx="10", pady="10")

        self.display_length_label = ctk.CTkLabel(self.app, text="")
        self.display_length_label.pack(padx="10")

        self.display_size_label = ctk.CTkLabel(self.app, text="")
        self.display_size_label.pack(padx="10")

        # Download buttons
        self.create_download_buttons()

        # Download finish label
        self.finish_label = ctk.CTkLabel(self.app, text="")
        self.finish_label.pack()

        # progress percentage and bar
        self.progress_percentage_label = ctk.CTkLabel(self.app, text="0%")
        self.progress_percentage_label.pack()

        self.progress_bar = ctk.CTkProgressBar(self.app, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx="10", pady="10")

    def create_download_buttons(self):
        download_frame = ctk.CTkFrame(self.app)
        download_frame.pack()

        buttons_info = [
            ("DOWNLOAD", self.download_video),
            ("Download Music / MP3", self.download_music),
            ("Download Playlist", self.download_playlist),
        ]

        for text, command in buttons_info:
            download_btn = ctk.CTkButton(download_frame, text=text, command=command)
            download_btn.pack(padx="10", pady="10", side="left")

    def save_download_path(self):
        download_path = self.path_entry.get()
        video_downloader.set_download_path(download_path)

    def download_video(self):
        youtube_link = self.link.get()
        resolution = self.resolution_input.get()
        threading.Thread(
            target=self.download_video_async, args=(youtube_link, resolution)
        ).start()

    def download_music(self):
        youtube_link = self.link.get()
        threading.Thread(target=self.download_music_async, args=(youtube_link,)).start()

    def download_video_async(self, youtube_link, resolution):
        if not youtube_link:
            self.finish_label.configure(
                text="Link cannot be empty",
                text_color="red",
                font=("Arial", 16, "bold"),
            )
            return

        get_details.fetch_details(
            youtube_link,
            self.finish_label,
            self.display_title_label,
            self.display_length_label,
            self.display_size_label,
            resolution,
        )

        video_downloader.start_download(
            youtube_link,
            self.finish_label,
            self.progress_percentage_label,
            self.progress_bar,
            resolution,
        )

    def download_music_async(self, youtube_link):
        if not youtube_link:
            self.finish_label.configure(
                text="Link cannot be empty",
                text_color="red",
                font=("Arial", 16, "bold"),
            )
            return

        get_details.fetch_details(
            youtube_link,
            self.finish_label,
            self.display_title_label,
            self.display_length_label,
            self.display_size_label,
            None,
        )

        music_downloader.start_download_music(
            youtube_link,
            self.finish_label,
            self.progress_percentage_label,
            self.progress_bar,
        )

    def download_playlist(self):
        pass


if __name__ == "__main__":
    app_instance = DownloaderApp()
    app_instance.app.mainloop()
