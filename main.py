import tkinter
import customtkinter
from pytube import YouTube
from src import video_downloader
import threading


class VideoDownloaderApp:
    def __init__(self):
        self.app = customtkinter.CTk()
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("dark-blue")
        self.app.geometry("800x600")
        self.app.title("TubeSaver")

        self.create_widgets()

    def create_widgets(self):
        # Heading
        heading = customtkinter.CTkLabel(
            self.app, text="TubeSaver", font=("Roboto", 32, "bold")
        )
        heading.pack(pady=20)

        # Download path frame
        path_frame = customtkinter.CTkFrame(self.app)
        path_frame.pack()

        path_label = customtkinter.CTkLabel(path_frame, text="Download Path: ")
        path_label.pack(side="left", padx="20")

        self.path_entry = customtkinter.CTkEntry(path_frame, width=200)
        self.path_entry.pack(side="left")

        # path save button
        path_save_button = customtkinter.CTkButton(
            self.app, text="Save path", command=self.save_download_path
        )
        path_save_button.pack(padx=10, pady=(20, 0))

        # title label
        title = customtkinter.CTkLabel(
            self.app, text="Insert a youtube video link to download"
        )
        title.pack(padx=10, pady=10)

        input_url_frame = customtkinter.CTkFrame(self.app)
        input_url_frame.pack()

        self.url_var = tkinter.StringVar()
        self.link = customtkinter.CTkEntry(
            input_url_frame,
            width=350,
            height=30,
            placeholder_text="Video url",
            placeholder_text_color="white",
            textvariable=self.url_var,
        )
        self.link.pack(side="left", padx="20")

        resolution_lable = customtkinter.CTkLabel(input_url_frame, text="Resolution: ")
        resolution_lable.pack(side="left", padx="10")

        self.res_value = tkinter.StringVar()
        self.resolution_input = customtkinter.CTkEntry(
            input_url_frame, width=40, height=30, textvariable=self.res_value
        )
        self.resolution_input.pack(side="left")

        # Video details labels
        self.video_details = customtkinter.CTkLabel(self.app, text="Video Details: ")
        self.video_details.pack(padx="10", pady="10")

        self.display_title_label = customtkinter.CTkLabel(self.app, text="")
        self.display_title_label.pack(padx="10", pady="10")

        self.display_length_label = customtkinter.CTkLabel(self.app, text="")
        self.display_length_label.pack(padx="10")

        self.display_resolution_label = customtkinter.CTkLabel(self.app, text="")
        self.display_resolution_label.pack(padx="10")

        self.display_size_label = customtkinter.CTkLabel(self.app, text="")
        self.display_size_label.pack(padx="10")

        # Download button
        download_btn = customtkinter.CTkButton(
            self.app, text="DOWNLOAD", command=self.download_video
        )
        download_btn.pack(padx="10", pady="10")

        # Download finish label
        self.finish_label = customtkinter.CTkLabel(self.app, text="")
        self.finish_label.pack()

        # progress percentage and bar
        self.progress_percentage_label = customtkinter.CTkLabel(self.app, text="0%")
        self.progress_percentage_label.pack()

        self.progress_bar = customtkinter.CTkProgressBar(self.app, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx="10", pady="10")

    def save_download_path(self):
        download_path = self.path_entry.get()
        video_downloader.set_download_path(download_path)

    def download_video(self):
        youtube_link = self.link.get()
        resolution = self.resolution_input.get()
        threading.Thread(
            target=self.download_video_async, args=(youtube_link, resolution)
        ).start()

    def download_video_async(self, youtube_link, resolution):
        if len(youtube_link) != 0:
            video_downloader.get_video_details(
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
        else:
            self.finish_label.configure(
                text="Youtube Video link cannot be empty",
                text_color="red",
                font=("Arial", 16, "bold"),
            )


if __name__ == "__main__":
    app_instance = VideoDownloaderApp()
    app_instance.app.mainloop()
