import requests
from collections import defaultdict
import json

def getMangaList():

    base_url = "https://api.mangadex.org"
    manga_id = "275c3ee8-bdeb-4070-a333-6add23a8415a"  # id do mangá do vagabond
    languages = ["pt-br"]


    apiResponse = requests.get(
        f"{base_url}/manga/{manga_id}/feed",
        params={
            "translatedLanguage[]": languages,
            "order[volume]": "desc",
            "order[chapter]": "desc"
        },
    )

    reorganizeManga(apiResponse.json()["data"])

    return reorganizeManga(apiResponse.json()["data"])

def reorganizeManga(mangalist):

    volumes = defaultdict(list)

    for chapter in mangalist:
        volume = chapter["attributes"]["volume"]
        volumes[volume].append(chapter)

    sorted_volumes = {
        volume: sorted(chapters, key=lambda x: int(x["attributes"]["chapter"]))
        for volume, chapters in sorted(volumes.items(), key=lambda x: int(x[0]))
    }

    formatted_output = json.dumps(sorted_volumes, indent=4)

    return formatted_output

print(getMangaList())
