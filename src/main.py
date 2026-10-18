import flet as ft
from System.KAS_IA_RELOD import carregamento, identificacao
from System.Procurar import compactar
from System.GerarLista import gerar
from System.Gerar_KAS_AI import prever
from System.Migrar import migracao

lista_dados = None
files = []
itens = []
agrupar_nome = True
agrupar_extesao = False
alternativaIA = False
IA = None

def agrupar_nex(e, page, outro):
    global agrupar_nome, agrupar_extesao
    src = e.control 
    src.checked = True
    agrupar_extesao = not agrupar_extesao
    agrupar_nome = not agrupar_nome
    print(agrupar_extesao, agrupar_nome)

    outro.checked = False
    page.update()

def check_item_clicked(e, page, outro, AI=None, alternativaIA_=False):
    global IA, alternativaIA
    src = e.control 
    src.checked = True
    IA = AI
    alternativaIA = alternativaIA_
    outro.checked = False
    page.update()

laptop = ft.PopupMenuButton(
        icon=ft.Icons.LAPTOP,
        icon_color="#FBB100",
        bgcolor='#402E15',
        tooltip=ft.Tooltip(
                    message="Escolha como você quer organizar",
                    bgcolor='#402E15',
                    text_style=ft.TextStyle(color=ft.Colors.WHITE),
                ),
        items=[
            item1menu := ft.PopupMenuItem(
                content=ft.Row(controls=[
                    ft.Icon(icon=ft.Icons.DRIVE_FILE_RENAME_OUTLINE_SHARP),
                    ft.Text("Agrupar por nome"),
                ]),
                checked=True,
            ),
            item2menu := ft.PopupMenuItem(
                content=ft.Row(controls=[
                    ft.Icon(icon=ft.Icons.EXTENSION),
                    ft.Text("Agrupar por extensões"),
                ]),
                checked=False,
            ),
        ]
    )

ia = ft.PopupMenuButton(
        icon=ft.Icons.PSYCHOLOGY,
        tooltip=ft.Tooltip(
                    message="Escolha a IA da sua preferencia",
                    bgcolor='#402E15',
                    text_style=ft.TextStyle(color=ft.Colors.WHITE),
                ),
        icon_color="#FBB100",
        bgcolor='#402E15',
        items=[
            kas := ft.PopupMenuItem(
                content=ft.Row(controls=[
                    ft.Icon(icon=ft.Icons.MEMORY),
                    ft.Text("KAS.AI"),
                ]),
                checked=True,
            ),
        ]
    )

icons = ft.Container(
                    expand=5,
                    padding=ft.Padding.only(left=10, right=10, bottom=9, top=8),
                    content=ft.Container(
                        expand=1,
                        bgcolor='#FBB100',
                        padding=1.5,
                        border_radius=10,
                        content=ft.Container(
                            expand=True,
                            bgcolor='#402E15',
                            border_radius=10,
                            content=ft.Row(
                                spacing=-3,
                                controls=[
                                    laptop,
                                    ia
                                ]
                            )
                        ),
                    ),
                )

botao_gerar = ft.Container(
    width=140,
    height=45,
    padding=1.5,
    on_click=lambda _: print("O usuário clicou em gerar"),
    alignment=ft.Alignment.CENTER,
    border_radius=15,
    bgcolor='#A6FF9E',
    content=ft.Container(
            expand=True,
            bgcolor="#2C3A1F",
            alignment=ft.Alignment.CENTER,
            border_radius=13,
            content=(texto_gerar := ft.Text(
                "Gerar",
                scale=2,
                font_family='Cascadia Code Regular',
                color="#99D4A0"
            )
        )
    )
)

botao_procurar = ft.Container(
    width=140,
    height=45,
    padding=1.5,
    on_click=lambda _: print("O usuário clicou em procurar"),
    alignment=ft.Alignment.CENTER,
    border_radius=15,
    bgcolor='#FFCF5C',
    content=ft.Container(
            expand=True,
            bgcolor="#603A04",
            alignment=ft.Alignment.CENTER,
            border_radius=13,
            content=(texto_gerar := ft.Text(
                "Procurar",
                scale=1.8,
                font_family='Cascadia Code Regular',
                color="#F7C858"
            )
        )
    )
)

botoes = ft.Container(
                    expand=10,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            botao_gerar,
                            botao_procurar
                        ]
                    )
                )

icons_buttons = ft.Container(
                            expand=True,
                            bgcolor='#402E15',
                            padding=ft.Padding.only(left=5, right=10, top=5, bottom=5),
                            border_radius=ft.BorderRadius.only(bottom_left=29, bottom_right=29),
                            content=ft.Row(
                                spacing=0,
                                controls=[
                                    icons,
                                    botoes
                                ]
                            )
                        )

arquivos_de_exibicao = ft.Container(
                                        expand=2,
                                        alignment=ft.Alignment.CENTER,
                                        content=ft.Container(
                                            expand=2,
                                            width=650,
                                            bgcolor='#FBB100',
                                            border_radius=56,
                                            padding=1.5,
                                            shadow = ft.BoxShadow(
                                                blur_radius=12,
                                                offset=ft.Offset(5, 5),
                                                blur_style=ft.BlurStyle.NORMAL,
                                                color=ft.Colors.with_opacity(0.5, '#000000'),
                                            ),
                                            content=ft.Container(
                                                expand=True,
                                                alignment=ft.Alignment(0,-0.3),
                                                bgcolor='#402E15',
                                                padding=5,
                                                border_radius=56,
                                                content=ft.Text(
                                                    "Arquivos de exibição",
                                                    scale=1.6,
                                                    weight=ft.FontWeight.BOLD
                                                )
                                            ),
                                        ),
                                    )

lista_pasta = ft.Container(
    expand=15,
    width=22900,
    content=ft.Text('Todos os arquivos da pasta selecionada serão exibidas aqui, A IA não organizarar de um ótima forma se os nomes dos arquivos não resumir o arquivo. Recomendamos que usem o modo extensão no icone de laptop.', opacity=0.5)
)

pastas = ft.Container(
                                expand=20,
                                bgcolor='#FBB100',
                                border_radius=25,
                                padding=1.5,
                                shadow = ft.BoxShadow(
                                        blur_radius=12,
                                        offset=ft.Offset(5, 5),
                                        blur_style=ft.BlurStyle.NORMAL,
                                        color=ft.Colors.with_opacity(0.5, '#000000'),
                                ),
                                content=ft.Container(
                                    expand=True,
                                    bgcolor='#402E15',
                                    padding=ft.Padding.only(left=10, right=10, bottom=10, top=5),
                                    border_radius=25,
                                    content=lista_pasta
                                ),
                            )

arquivos_migrar = ft.Container(
                                expand=2,
                                border_radius=15,
                                on_click=lambda _: print("O usuário clicou em migrar!"),
                                alignment=ft.Alignment.CENTER,
                                bgcolor='#FFB56D',
                                shadow = ft.BoxShadow(
                                        blur_radius=12,
                                        offset=ft.Offset(5, 5),
                                        blur_style=ft.BlurStyle.NORMAL,
                                        color=ft.Colors.with_opacity(0.5, '#000000'),
                                ),
                                content=ft.Text(
                                    "Migrar",
                                    scale=1.8,
                                    font_family='Cascadia Code SemiBold'
                                )
                            )

migrar = ft.Column(
                        spacing=9,
                        controls=[
                            arquivos_de_exibicao,
                            pastas,
                            arquivos_migrar,
                        ]
                    )

def mudar(dados):
    global lista_dados
    lista_dados = dados

'''lista_dados = [
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

lista_pasta.content = gerar(page, lista_dados, mudar)
page.update()'''

def carregando_itens():
    status_kas = carregamento()

    if status_kas['status'] == '400':
        return status_kas
    else:
        return {'status':'200', 'mensagem':'Modelo carregado com sucesso!'}
        
def desable(botao, opacidade, page):
    if not botao.disabled == True:
        botao.disabled = True
        botao.opacity = opacidade
    else:
        botao.disabled = False
        botao.opacity = 1
    page.update()

def main(page: ft.Page):
    global texto_gerar
    page.title = 'OrganizAI'
    page.window.width = 800
    page.window.height = 600
    page.locale_configuration = ft.LocaleConfiguration(supported_locales=[ft.Locale("pt", "BR")], current_locale=ft.Locale("pt", "BR"))
    page.padding = 0
    page.fonts = {
        "Cascadia Code SemiBold": "https://github.com/PvKa732/hospedagem/raw/refs/heads/main/static/CascadiaCode-SemiBold.ttf",
        "Cascadia Code Regular": "https://github.com/PvKa732/hospedagem/raw/refs/heads/main/static/CascadiaCode-Regular.ttf"
    }

    def carregar_noasync(fuction):
        def wrapper():
            lista_pasta.content = ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=(
                    ft.ProgressRing(scale=1.5, color='#FBB100')
                )
            )
            page.update()
            fuction()
        return wrapper

    def carregar(fuction):
        async def wrapper():
            lista_pasta.content = ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=(
                    ft.ProgressRing(scale=1.5, color='#FBB100')
                )
            )
            await fuction(None)
        return wrapper

    async def pick_text_file(e):
        global files
        files = await ft.FilePicker().get_directory_path()

        if files:
            @carregar
            async def posfile(e):
                global files, lista_dados, itens
                retorna = compactar(page, files)
                lista_dados = retorna[0]
                itens = retorna[1]
                lista_pasta.content = gerar(page, lista_dados, mudar, itens)
                
                if arquivos_migrar.disabled == False:
                    desable(arquivos_migrar, 0.8, page)

                if botao_gerar.disabled == True:
                    desable(botao_gerar, 0.6, page)
            await posfile()
            page.update()
    
    @carregar_noasync
    def KAS_AI():
        dicionarios = prever(page, itens, agrupar_nome, agrupar_extesao, alternativaIA, IA)
        lista_pasta.content = gerar(page, dicionarios, mudar, itens)

        if arquivos_migrar.disabled == True:
            desable(arquivos_migrar, 0.8, page)
        page.update()

    def fazer_migracao(lista_dados, files, itens):
        status = migracao(lista_dados, files, itens)

        if status == '400':
            print(status['Exeception'])
        else:
            desable(botao_gerar, 0.6, page)
            desable(arquivos_migrar, 0.8, page)
            lista_pasta.content=ft.Text('Todos os arquivos da pasta selecionada serão exibidas aqui, A IA não organizarar de um ótima forma se os nomes dos arquivos não resumir o arquivo. Recomendamos que usem o modo extensão no icone de laptop.', opacity=0.5)
            page.update()

    status_ia, status_kas = carregando_itens()
    desable(botao_gerar, 0.6, page)
    desable(arquivos_migrar, 0.8, page)
    botao_procurar.on_click = pick_text_file
    botao_gerar.on_click = lambda _: KAS_AI()
    item1menu.on_click = lambda e: agrupar_nex(e, page, item2menu)
    item2menu.on_click = lambda e: agrupar_nex(e, page, item1menu)
    arquivos_migrar.on_click = lambda e: fazer_migracao(lista_dados, files, itens)

    principal = ft.SafeArea(
        expand=True,
        content=ft.Container(
            expand=True,
            bgcolor='#46361E',
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Container(
                        expand=2,
                        bgcolor='#FBB100',
                        padding=1.5,
                        border_radius=ft.BorderRadius.only(bottom_left=29, bottom_right=29),
                        content=icons_buttons
                    ),
                    ft.Container(
                        expand=14,
                        padding=ft.Padding.only(left=7, right=7, bottom=10),
                        content=migrar
                    ),
                ]
            )
        )
    )

    page.add(
        principal
    )


ft.run(main)
