import torch
import torch.nn as nn
import string
import json
import os
from pathlib import Path

CAMINHO_CATETXT = Path(__file__).parent / "catetxt.txt"
CAMINHO_DATATXT = Path(__file__).parent / "datatxt.txt"
CAMINHO_CEREBRO = Path(__file__).parent / "cerebro_kas_ia.pth"
CAMINHO_CEREBRO_EXTENSAO = Path(__file__).parent / "cerebro_kas_ia_read.pth"
TAMANHO_MAX = 30
modelo = None
modelo_extesao = None

alfabeto = ' ' + string.ascii_lowercase + string.digits + string.punctuation + 'áéíóúâêôãõç'
tokenizador = {letra: i for i, letra in enumerate(alfabeto)}
nomes_categorias = []
nomes_categorias2 = []
id_outros = -1


def carregamento():
    global modelo, modelo_extesao, nomes_categorias, nomes_categorias2, id_outros
    try:
        with open(CAMINHO_CATETXT, 'r', encoding='utf-8') as f:
            try:
                lista_categorias = json.load(f)
            except:
                import ast
                f.seek(0)
                lista_categorias = ast.literal_eval(f.read())
                
        with open(CAMINHO_DATATXT, 'r', encoding='utf-8') as f:
            try:
                lista_categorias2 = json.load(f)
            except:
                import ast
                f.seek(0)
                lista_categorias2 = ast.literal_eval(f.read())
                

        nomes_categorias = [cat[0] for cat in lista_categorias]
        for iten in lista_categorias2:
            categoria = iten[1].title()
            if categoria not in nomes_categorias2:
                nomes_categorias2.append(categoria)
        id_outros = nomes_categorias.index("Outros") if "Outros" in nomes_categorias else -1
    except:
        return {'status':'400', 'mensagem':f'Erro ao encontrar o arquivo {CAMINHO_CATETXT}'}

    try:
        modelo = nn.Sequential(
            nn.Embedding(num_embeddings=len(alfabeto), embedding_dim=16),
            nn.Flatten(),
            nn.Linear(TAMANHO_MAX * 16, 128),
            nn.ReLU(),
            nn.Linear(128, len(nomes_categorias))
        )
        # Modificado: Mantido num_embeddings fixo em 69 explicitamente para o modelo_extensao carregar o arquivo antigo sem erros
        modelo_extesao = nn.Sequential(
            nn.Embedding(num_embeddings=69, embedding_dim=8), 
            nn.Flatten(),                                     
            nn.Linear(80, len(nomes_categorias2)) 
        )
    except Exception as e:
        return {'status':'400', 'mensagem':'Erro ao criar o cerébro'}

    try:
        modelo.load_state_dict(torch.load(CAMINHO_CEREBRO, weights_only=True))
        modelo.eval()

        modelo_extesao.load_state_dict(torch.load(CAMINHO_CEREBRO_EXTENSAO, weights_only=True))
        modelo_extesao.eval()
        return {'status':'200', 'mensagem':'Arquivo carregado com sucesso!'}
    except Exception as e:
        return {'status':'400', 'mensagem':'Erro ao carregar o cerebro', 'Exception': e}


def transformar_em_tensor(texto, tamanho_maximo=TAMANHO_MAX):
    tokens = [tokenizador.get(letra, 0) for letra in texto.lower()]
    while len(tokens) < tamanho_maximo:
        tokens.append(0)
    tokens = tokens[:tamanho_maximo]
    return torch.tensor(tokens)

def identificacao(arquivo, extensao=False):
    if not arquivo:
        return {'status':'400', 'mensagem':'Arquivo vazio'}
        
    if extensao == False:
        with torch.no_grad():
            tensor = transformar_em_tensor(arquivo, tamanho_maximo=TAMANHO_MAX).unsqueeze(0)
            saida_ia = modelo(tensor)
            
            probabilidades = torch.softmax(saida_ia, dim=1)
            maior_prob, escolha_id = torch.max(probabilidades, dim=1)
            
            maior_prob = maior_prob.item()
            escolha_id = escolha_id.item()
            
            categoria_escolhida = nomes_categorias[escolha_id]
            
            if maior_prob < 0.50 and id_outros != -1:
                return {'status':'200', 'mensagem':'Outros', 'probabilidade':maior_prob}
            else:
                return {'status':'200', 'mensagem':categoria_escolhida, 'probabilidade': maior_prob}
    else:
        with torch.no_grad():
            tensor = transformar_em_tensor(arquivo, tamanho_maximo=10).unsqueeze(0)
            saida_ia = modelo_extesao(tensor)
            escolha_id = torch.argmax(saida_ia).item()
            nome_escolhido = nomes_categorias2[escolha_id]
            return {'status':'200', 'mensagem':nome_escolhido}

if __name__ == "__main__":
    status = carregamento()
    print(status['mensagem'], "/ Status:", status['status'])
    if status['status'] == '200':
        print(identificacao(input("Digite o nome do arquivo: ")))