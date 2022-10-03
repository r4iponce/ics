from hashlib import sha256
from os import getenv
from os.path import exists
from shutil import move

import requests
from dotenv import load_dotenv


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


def main(token: str, download_location: str) -> None:
    if exists(download_location):
        temp_download_file = "temp_calendar.ics"
        download_calendar(token, download_location)
        if verify_version(download_location, temp_download_file):
            print("No new version")
        else:
            move(temp_download_file, download_location)
            print("New version downloaded")
    else:
        print("File downloaded")
        download_calendar(token, download_location)


if __name__ == "__main__":
    load_dotenv()
    main(str(getenv('TOKEN')), str(getenv("DOWNLOAD_LOCATION")))
