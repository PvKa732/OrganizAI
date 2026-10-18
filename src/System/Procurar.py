import flet as ft
from pathlib import Path
import os

def pasta_lista(lista):
    itens = []
    for iten in lista:
        diretorio_original = iten[0]
        diretorio = iten[0] + iten[1]
        extensao = iten[1]
        nome, nome_original = Path(diretorio_original).name, Path(diretorio).name
        pastas = False
        if not extensao:
            try:
                caminho_pasta = Path(diretorio)
                pastas = [os.path.splitext(x) for x in caminho_pasta.iterdir()]
                lista_ = pasta_lista(pastas)
                itens.append({'icon': ft.Icons.FOLDER, 'nome': nome_original, 'lista': lista_})
            except Exception as e:
                    print(e)
        else:
            itens.append({'icon': ft.Icons.INSERT_DRIVE_FILE, 'nome': nome_original})
    return itens

def compactar(page, caminho):
    caminho_ = Path(caminho)
    if caminho_.exists():
        itens = [os.path.splitext(x) for x in caminho_.iterdir()]
        dicionarios = []
        for iten in itens:
            diretorio_original = iten[0]
            diretorio = iten[0] + iten[1]
            extensao = iten[1]
            nome, nome_original = Path(diretorio_original).name, Path(diretorio).name
            pastas = False

            if not extensao:
                try:
                    caminho_pasta = Path(diretorio)
                    pastas = [os.path.splitext(x) for x in caminho_pasta.iterdir()]
                    lista = pasta_lista(pastas)
                    dicionarios.append({'icon': ft.Icons.FOLDER, 'nome': nome_original, 'lista': lista})
                except Exception as e:
                    print(e)
            else:
                dicionarios.append({'icon': ft.Icons.INSERT_DRIVE_FILE, 'nome': nome_original})
        return (dicionarios, itens)
        