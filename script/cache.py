import requests
from pathlib import Path


def get_html_page(localFile: Path, url: str):

    html = None

    if localFile.exists():
        # print("Loading html from cache...")

        with open(localFile, "rb") as f:
            html = f.read().decode()

    else:
        # print("Requesting html from server...")
        res = requests.get(url)
        html = res.text

        with open(localFile, "wb") as f:
            f.write(res.text.encode())

    return html
