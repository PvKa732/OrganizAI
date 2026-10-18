from pathlib import Path
import shutil
import os

def migracao(lista_dados, files, itens):
    # lista_dados => com as categorias e os itens dentro
    # files => o pai com todas as pastas
    # itens => caminho para pasta de cada um
    # criando uma pasta => Path.mkdir()
    # movendo um arquivo => shutil.move('caminho/arquivo.extensao', 'pasta/arquivo.extensao')

    categorias = []
    caminho_padrao = Path(files)
    itens_atuais = [{'diretorio': iten[0] + iten[1], 'nome': Path(iten[0] + iten[1]).name} for iten in [os.path.splitext(x) for x in caminho_padrao.iterdir()]]
    try:
        for iten in lista_dados:
            try:
                test = iten['lista']

                nome = iten['nome']
                lista = iten['lista']
                for iten_ in itens_atuais:
                    if not iten_['nome'] == nome:
                        if not {'nome': nome, 'lista': lista} in categorias:
                            categorias.append({'nome': nome, 'lista': lista})
            except:
                pass
        
        for categoria in categorias:
            caminho = Path(caminho_padrao / categoria['nome'])
            Path.mkdir(parents=caminho_padrao, self=caminho)
            for iten_z in categoria['lista']:
                nome__ = iten_z['nome']
                diretorio_original = Path(caminho_padrao / iten_z['nome'])
                direitorio_proximo = Path(caminho_padrao / categoria['nome'] / iten_z['nome'])
                shutil.move(diretorio_original, direitorio_proximo)

        return {'status': '200', 'mensagem': 'Migração concluida'}
    except Exception as e:
        return {'status': '400', 'mensagem': 'Algo deu errado', 'Exeception': e}
    