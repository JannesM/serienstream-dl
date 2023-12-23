

def decode_url_identifier(url: str):

    if len(url.split("/")) == 5:

        season = int(url.split("-")[-1])
        return (season, -1)

    elif len(url.split("/")) == 6:

        season = int(url.split("/")[-2].split("-")[-1])
        episode = int(url.split("/")[-1].split("-")[-1])
        return (season, episode)


def format_filename(s):
    invalid_chars = "\/:*?\"<>|"
    filename = ''.join(c for c in s if c not in invalid_chars)
    return filename