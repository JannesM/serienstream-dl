import requests
import re
import multiprocessing
import json

from bs4 import BeautifulSoup as Soup
from progress.bar import Bar
from pathlib import Path
from urllib.parse import quote
from dataclasses import dataclass
import m3u8_To_MP4

import utils
import cache

DOMAIN = "https://s.to"

def analyze_season(args):
    local_file, season_url = args

    seasonID, _ = utils.decode_url_identifier(season_url)

    # load web page from cache or request it
    html = cache.get_html_page(
        local_file / f"season-{seasonID}.html", DOMAIN+season_url)
    soup = Soup(html, "html.parser")

    # filter links to episodes
    episodes = set([a['href'] for a in soup.find_all("a", href=True)
                    if len(a['href'].split("/")) == 6 and a['href'].startswith("/serie/stream")])

    return episodes


def analyze_episode(args):
    local_file, episode_url = args

    seasonID, episodeID = utils.decode_url_identifier(episode_url)

    # load web page from cache or request it
    html = cache.get_html_page(
        local_file / f"season-{seasonID}-episode-{episodeID}.html", DOMAIN+episode_url)
    soup = Soup(html, "html.parser")

    # find VOE redirect url
    redirect_url = soup.find("div", attrs={"class": "hosterSiteVideo"}).find(
        "ul").find_all("li")[0].find("a", href=True)["href"]
    
    title = soup.find("span", attrs={"class": "episodeGermanTitle"}).text
    # print(title)

    return (episode_url, redirect_url, title)


def download_video(args):
    local_path, episode_url, redirect_url, title = args

    seasonID, episodeID = utils.decode_url_identifier(episode_url)
    name = f"{utils.format_filename(title)} S{seasonID}E{episodeID}"

    if (local_path / f"{name}.mp4").exists():
        print(f"Episode {episodeID} of Season {seasonID} already downloaded!")
        return
    
    with requests.Session() as session:

        res = session.get(DOMAIN+redirect_url)

        # remove whitespaces and line breaks
        html = res.text.replace(" ", "").replace("\r\n", "").replace(
            "\r", "").replace("\n", "").replace("\t", "")

        # search hls m3u8 master url
        pattern = r"(?<=varsources={'hls':').*(?=','video_height)"
        query = re.search(pattern, html)
        master_url = query.group()
        # print("Master:", master_url)

        m3u8_To_MP4.multithread_download(master_url, mp4_file_dir=local_path.absolute(), mp4_file_name=name)


@dataclass
class Scraper:

    # external
    base_url: str
    ls_path: Path

    # internal
    mapping: list[tuple[str, str, str]] = None
    season_count: int = 0
    episode_count: int = 0

    def analyze(self):
        """Pulls meta data from base_url. May issue a GET request."""

        # create scraper path
        scraper_path = self.ls_path / self.base_url.split("/")[-1] / "cache"
        scraper_path_html = self.ls_path / \
            self.base_url.split("/")[-1] / "cache" / "html"

        scraper_path.mkdir(parents=True, exist_ok=True)
        scraper_path_html.mkdir(parents=True, exist_ok=True)

        # if self.import_mapping((scraper_path / "mapping.json")):
        #     print("Using cached mapping...")
        #     return

        # load web page from cache or request it
        html = cache.get_html_page(scraper_path / "index.html", self.base_url)
        soup = Soup(html, "html.parser")

        # filter links to seasons
        seasons = set([a['href'] for a in soup.find_all("a", href=True)
                       if len(a['href'].split("/")) == 5 and a['href'].startswith("/serie/stream")])
        self.season_count = len(seasons)

        # fetch season data for each season
        tasks = [(scraper_path_html, s) for s in seasons]
        episodes = list()

        with multiprocessing.Pool(3) as pool:
            with Bar("Indexing Seasons...", suffix="%(index)d/%(max)d", max=self.season_count) as bar:
                for result in pool.imap_unordered(analyze_season, tasks):
                    episodes += result
                    bar.next()

        self.episode_count = len(episodes)

        tasks = [(scraper_path_html, e) for e in episodes]
        self.mapping = list()

        with multiprocessing.Pool(20) as pool:
            with Bar("Indexing Episodes...", suffix="%(index)d/%(max)d", max=self.episode_count) as bar:
                for result in pool.imap_unordered(analyze_episode, tasks):
                    self.mapping.append(result)
                    bar.next()

        self.mapping = sorted(self.mapping, key=lambda d: (int(d[0].split(
            "/")[-2].split("-")[-1]), int(d[0].split("/")[-1].split("-")[-1])))

        self.export_mapping(scraper_path / "mapping.json")

        print(
            f"Found {self.season_count} seasons and {self.episode_count} episodes.")

    def export_mapping(self, path):

        result = list()

        for episode_url, redirect_link, title in self.mapping:
            result.append({
                "episode_url": episode_url,
                "redirect_link": redirect_link,
                "title": title,
            })

        with open(path, "w") as f:
            f.write(json.dumps(result))

    def import_mapping(self, path):

        if not path.exists():
            return False

        self.mapping = list()

        with open(path, "r") as f:
            data = json.loads(f.read())

            for mapping in data:
                self.mapping.append(
                    (mapping["episode_url"], mapping["redirect_link"], mapping["title"]))

        return True

    def download(self):

        scraper_path = self.ls_path / self.base_url.split("/")[-1]
        tasks = list()

        for episode_url, redirect_link, title in self.mapping:
            seasonID, _ = utils.decode_url_identifier(episode_url)
            season_path = scraper_path / f"Season {seasonID}"
            season_path.mkdir(parents=True, exist_ok=True)

            tasks.append((
                season_path,
                episode_url,
                redirect_link,
                title
            ))
        
        
        for i, args in enumerate(tasks[:1]):
            seasonID, episodeID = utils.decode_url_identifier(args[1])
            print(f"\n############# Downloading S{seasonID}E{episodeID} {i+1}/{len(tasks)} #############\n")
            download_video(args)
