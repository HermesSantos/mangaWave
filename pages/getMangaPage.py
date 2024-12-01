import flet as ft
from controller.MangaApiClient import MangaApiClient
from controller.Helpers import Helpers

def main(page: ft.Page):

    inputManga = ft.TextField(
        label="Nome Do Mangá",
        bgcolor='#3d444d',
        color='#ffffff'
    )

    progressRow = ft.Row(
        controls=[
            ft.ProgressRing(width=16, height=16, stroke_width=2), 
            ft.Text("Procurando Seu mangá...")
        ],
        visible=False
    )

    pageTitle = ft.Text(
        value='Resultados para Naruto', 
        size=30,
        visible=False
    )

    resultsManga = ft.Row(
        controls=[],
        wrap=True,
        visible=False,
        scroll=ft.ScrollMode.AUTO,
        height=0.7 * page.window_height
    )

    def getMangaList(offset=0):
        progressRow.visible = True
        resultsManga.visible = False
        page.update()

        mangaData = MangaApiClient.getManga(inputManga.value, offset)
        if mangaData:
            printResult(inputManga.value, mangaData)
        else:
            pageTitle.value = f"Resultado de {inputManga.value}"

        progressRow.visible = False
        pageTitle.visible = True
        page.update()

    def navegatePaginate(page_number, mangaData):
        offset = (page_number - 1) * mangaData['limit']
        getMangaList(offset)  
    def goToList(e):
        print(e) 

    def printResult(title, result):
        pageTitle.value = f"Resultado de {title} ({result['total']} resultado{'s' if result['total'] > 1 else ''})"
        paginate = Helpers.paginateGenerate(result['total'], result['limit'], result['offset'])

        resultsManga.controls = [
            ft.Container(
                on_click=lambda e, index=index: goToList(index),
                content=ft.Column([
                    ft.Image(src=manga['cover_art'], width=0.20 * page.window_width, height=300),
                    ft.Text(manga['title'], size=18),
                    ft.Text(f"Idiomas Disponiveis: {', '.join([lang for lang in manga['lenguangesEnsabled'] if lang in ['en', 'pt-br']])}", size=14)
                ], 
                alignment="center", horizontal_alignment="center"),
                padding=10,
                width=0.32 * page.window_width,
                height=450,
                border_radius=10,
                bgcolor="#3d444d"
            ) for index, manga in result['data'].items()
        ]

        if paginate and paginate[0] != paginate[1]:
            buttonsPage = [
                ft.ElevatedButton(
                    text=str(pageNumber),
                    on_click=lambda e, page_number=pageNumber: navegatePaginate(page_number, result) 
                ) for pageNumber in range(paginate[0], paginate[1] + 1)
            ]
            resultsManga.controls.append(
                ft.Row(
                    controls=buttonsPage
                )
            )

        resultsManga.visible = True

    page.views.append(
        ft.View(
            route='/mangas-get',
            controls=[
                ft.AppBar(
                    title=ft.Text('MangaWave - Buscar Manga'),
                    leading=ft.IconButton(
                        icon="ARROW_BACK_IOS",
                        on_click=lambda _: page.go('/'),
                    ),
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=inputManga,
                            width=0.4 * page.window_width,
                        ),
                        ft.ElevatedButton(
                            text="Pesquisar", 
                            on_click=lambda e: getMangaList(0),
                            icon="SEARCH",
                        )
                    ]
                ),
                progressRow,
                pageTitle,
                resultsManga
            ]
        )
    )