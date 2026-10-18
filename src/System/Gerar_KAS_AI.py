import flet as ft
from pathlib import Path
import os
from System.Procurar import pasta_lista
from System.KAS_IA_RELOD import identificacao
from System.Outra_IA import alternativa

def prever(page, itens, agrupar_nome, agrupar_extesao, AlternativaIA, IA=None):
    if itens:
        dicionarios = []
        categorias_nomes = []
        categorias = []
        for iten in itens:
            caminho_ = Path((iten[0] + iten[1]))
            if caminho_.exists():
                diretorio_original = iten[0]
                diretorio = iten[0] + iten[1]
                extensao = iten[1]
                nome, nome_original = Path(diretorio_original).name, Path(diretorio).name
                if not AlternativaIA == True:
                    if not agrupar_extesao == True:
                        status = identificacao(nome)
                    else:
                        status = identificacao(extensao.replace(".", ""), extensao=True)
                else:
                    if not agrupar_extesao == True:
                        status = AlternativaIA(nome)
                    else:
                        status = AlternativaIA(extensao.replace(".", ""), extensao=True)
                if not int(status['status']) == 400:
                    if categorias:
                        if not status['mensagem'] in categorias_nomes:
                            categorias_nomes.append(status['mensagem'])
                            categorias.append({'nome': status['mensagem'], 'lista': [{'nome': nome_original, 'diretorio': diretorio}]})
                        else:
                            for i, iten_ in enumerate(categorias):
                                if iten_['nome'] == status['mensagem']:
                                    categorias[i]['lista'].append({'nome': nome_original, 'diretorio': diretorio})
                    else:
                        categorias_nomes.append(status['mensagem'])
                        categorias.append({'nome': status['mensagem'], 'lista': [{'nome': nome_original, 'diretorio': diretorio}]})
        for iten in categorias:
            lista__ = []
            for x in iten['lista']:
                diretorio_ = Path(x['diretorio'])
                try:
                    itens = [os.path.splitext(x) for x in diretorio_.iterdir()]
                    lista_ = []
                    for iten_ in itens:
                        diretorio_original = iten_[0]
                        diretorio = iten_[0] + iten_[1]
                        extensao = iten_[1]
                        nome, nome_original = Path(diretorio_original).name, Path(diretorio).name
                        pastas = False
                        if not extensao:
                            try:
                                print(nome_original)
                                caminho_pasta = Path(diretorio)
                                pastas = [os.path.splitext(x) for x in caminho_pasta.iterdir()]
                                lista = pasta_lista(pastas)
                                print(nome_original)
                                lista_.append({'icon': ft.Icons.FOLDER, 'nome': nome_original, 'lista': lista})
                            except Exception as e:
                                print(e)
                        else:
                            lista_.append({'icon': ft.Icons.INSERT_DRIVE_FILE, 'nome': nome_original})
                    lista__.append({'icon': ft.Icons.FOLDER, 'nome': x['nome'], 'lista': lista_})
                except:
                    lista__.append({'icon': ft.Icons.INSERT_DRIVE_FILE, "nome": x['nome']})

            dicionarios.append({'icon': ft.Icons.FOLDER, "nome": iten['nome'], 'lista': lista__})
        return dicionarios
