import requests
from pathlib import Path
import json
from Helpers import Helpers

base_url = "https://api.mangadex.org"

class MangaApiClient: 
    
    # Busca de mangás em geral
    def getManga(title):

        response = requests.get(
            f"{base_url}/manga",
            params={
                "title": title
            }
        )

        customResponse = Helpers.responseCustom(response.json())

        formatted_output = json.dumps(customResponse, indent=4)

        return formatted_output
    
    # Método que busca todos os mangás disponivel do títuloda busca
    def getMangaList(manga_id):

        apiResponse = requests.get(
            f"{base_url}/manga/{manga_id}/feed",
            params={
                "translatedLanguage[]": ["pt-br"],
                "order[volume]": "desc",
                "order[chapter]": "desc"
            },
        )

        responseWithdiretory = Helpers.diretoryCreate(apiResponse)

        return json.dumps(responseWithdiretory, indent=4)
    
    # Esse méotodo busca as paginas relacionada ao capitulo do mangá
    def getMangasPages(hash):

        response = requests.get(
            f"{base_url}/at-home/server/{hash}"
        )

        response = response.json()
        response = Helpers.pagesUrl(response["chapter"])

        return response
    