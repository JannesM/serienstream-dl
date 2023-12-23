from pathlib import Path
from urllib.parse import quote
import utils
import json
import os
import re

BASE = Path("./out/hawaii-five-0")
MAPPING = list[tuple[int, int, str]]

OK = 1
NOT_FOUND = 2
UNCHECKED = 3


def get_season_count(mapping):
    seasons = list(set([x[0] for x in mapping]))

    return len(seasons)


def get_episode_count(mapping, season):
    episodes = list(set([x[1] for x in mapping if x[0] == season]))

    return len(episodes)


if __name__ == "__main__":

    with open(BASE / "cache" / "mapping.json") as f:

        data = json.loads(f.read())
        MAPPING = list()

        for e in data:
            seasonID, episodeID = utils.decode_url_identifier(e['episode_url'])
            row = (seasonID, episodeID, e['title'])
            MAPPING.append(row)

    # create grouping
    grouping = dict()
    for (seasonID, episodeID, title) in MAPPING:
        try:
            grouping[seasonID].append((episodeID, title))
        except KeyError:
            grouping[seasonID] = [(episodeID, title)]

    # file mapping
    for seasonID in range(1, get_season_count(MAPPING)+1):
        content_list = grouping[seasonID]

        not_found = list()
        unknown = list()

        path = BASE / f"Season {seasonID}"

        _, _, files = [x for x in os.walk(path)][0]

        print(f"Season {seasonID}:")

        for episodeID, title in content_list:

            epsiode_path = path / f"{quote(title)} S{seasonID}E{episodeID}.mp4"
            if not epsiode_path.exists():
                print(f"\tMissing file: {title} S{seasonID}E{episodeID}.mp4")
                continue

            new_epsiode_path = path / f"{title} S{seasonID}E{episodeID}.mp4"
            
            os.rename(epsiode_path, new_epsiode_path)

        # for file in files:

        #     pattern = r"S{1}\d{1,2}E{1}\d{1,2}"
        #     if not re.search(pattern, file):
        #         print(f"\tUnknown file: {file}")
