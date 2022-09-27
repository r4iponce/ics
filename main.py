from hashlib import sha256
from os.path import exists
from shutil import move

import requests

from config import DOWNLOAD_LOCATION, TOKEN


def get_file_hash(file_to_hash: str) -> str:
    with open(file_to_hash, "rb") as file:
        return sha256(file.read()).hexdigest()


def verify_version(file1: str, file2: str) -> bool:
    return bool(get_file_hash(file1) == get_file_hash(file2))


def download_calendar(token: str, download_path: str) -> None:
    headers = {"Authorization": token}
    get = requests.get(
        "https://portail.henallux.be/api/plannings/my/ical", headers=headers, timeout=5
    )
    with open(download_path, "wb") as file:
        file.write(get.content)


if __name__ == "__main__":
    if exists(DOWNLOAD_LOCATION):
        TEMP_DOWNLOAD_FILE = "temp_calendar.ics"
        download_calendar(TOKEN, TEMP_DOWNLOAD_FILE)
        if verify_version(DOWNLOAD_LOCATION, TEMP_DOWNLOAD_FILE):
            print("No new version")
        else:
            move(TEMP_DOWNLOAD_FILE, DOWNLOAD_LOCATION)
            print("New version downloaded")
    else:
        print("File downloaded")
        download_calendar(TOKEN, DOWNLOAD_LOCATION)
