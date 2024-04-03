import os
import platform

DOWNLOAD_PATH = None


# Function to determine the default download path
def get_default_download_path():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.path.expanduser("~"), "Downloads")
    elif system == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Downloads")
    elif system == "Linux":
        return os.path.join(os.path.expanduser("~"), "Downloads")
    else:

        return os.path.expanduser("~")


DOWNLOAD_PATH = get_default_download_path()


# Function to set the download path
def set_download_path(path):
    """
    Set the download path for the downloaded files.

    Args:
        path (str): The path where the files will be downloaded.
    """
    global DOWNLOAD_PATH
    if path:
        DOWNLOAD_PATH = path
    else:
        DOWNLOAD_PATH = get_default_download_path()
