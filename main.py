import requests

from config import TOKEN


def get_calendar(token: str) -> None:
    headers = {'Authorization': token}
    get = requests.get('https://portail.henallux.be/api/plannings/my/ical',
                       headers=headers, timeout=5)
    with open("calendar.ics", "wb") as file:
        file.write(get.content)
    print("Downloaded")


if __name__ == "__main__":
    get_calendar(TOKEN)
