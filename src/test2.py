import flet as ft
from System.GerarLista import gerar

def main(page: ft.Page):
    def mudar(dados):
        global lista_dados
        lista_dados = dados


    lista_dados = [
        {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'video4k.mp4'},
        {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'python.py'},
        {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'texto.txt'},
        {'icon': ft.Icons.FOLDER, "nome": 'Documentos', 'lista': [
            {'icon': ft.Icons.FOLDER, "nome": 'E-books', 'lista': [
                {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'Arqui24vo_2026.pdf'},
                {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": '20225.pdf'},
                {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": '241.pdf'}
            ]},
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'Arquivo_2026.pdf'},
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": '2025.pdf'},
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": '24.pdf'},
        ]},
        {'icon': ft.Icons.FOLDER, "nome": 'Audios', 'lista': [
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'pronunciamento.mp3'},
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'musica.mp3'},
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'radio.mp3'}
        ]},
        {'icon': ft.Icons.FOLDER, "nome": 'Aplicativos', 'lista': [
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'Counter Strike 2.exe'},
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'CDD.exe'},
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'Discord.apk'}
        ]},
        {'icon': ft.Icons.FOLDER, "nome": 'Outros', 'lista': [
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'cs2.mp4'},
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'teste (1).exe'},
            {'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": 'txtdata.txt'}
        ]},
    ]

    page.add(gerar(page, lista_dados, mudar))

ft.run(main)