from pathlib import Path
from scraper import Scraper

BASE_URL = "https://aniworld.to/anime/stream/shangri-la-frontier"
OUT_PATH = Path("./out")

if __name__ == "__main__":

    # create output folder
    OUT_PATH.mkdir(exist_ok=True)

    # initialize scraper
    scraper = Scraper(BASE_URL, OUT_PATH)
    print("Starting Scraper...")
    scraper.analyze()
    print("Starting Downloader...")
    scraper.download()
