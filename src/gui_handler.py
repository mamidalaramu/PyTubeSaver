# Define the update_download_status function
def update_download_status(message, label):
    if message == "Download Complete!":
        text_color = "green"
    else:
        text_color = "red"
    label.configure(text=message, text_color=text_color)


# Define the update_progress_bar function
def update_progress_bar(percentage, progress_percentage_label, progress_bar):
    progress_percentage_label.configure(text=f"{percentage}%")
    progress_percentage_label.update()
    progress_bar.set(float(percentage) / 100)


# Define the update_display_details function
def update_display_details(
    title,
    length_min,
    length_sec,
    video_size_mb,
    display_title_label,
    display_length_label,
    display_size_label,
):

    display_title_label.configure(text="Title:  " + str(title))
    display_length_label.configure(
        text="Length:  " + f"{length_min} minutes and {length_sec} seconds"
    )
    display_size_label.configure(text="Size:  " + str(video_size_mb))
