import flet as ft

def gerar(page, dados, mudar, itens):

    def chamar(e):
        data = e.control.parent.parent.data

        def confirme(textvalue):
            page.pop_dialog()
            lista_dados[data['index']]['nome'] = textvalue
            lista_visual.controls.clear()
            render()
            page.update()

        nome_arquivo = ft.AlertDialog(
            title=ft.Text("Digite um nome para pasta.", style=ft.TextStyle(color='#FBB100', weight=ft.FontWeight.W_700,)),
            bgcolor='#402E15',
            content=(text := ft.TextField(
                border_radius=30,
                width=100,
                cursor_color='#FBB100',
                color='#FBB100',
                border_color='#FBB100',
                label_style=ft.TextStyle(
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color='#FBB100'
                )
            )),
            actions=[
                ft.TextButton(content=ft.Text("Confirme", style=ft.TextStyle(color='#FBB100', weight=ft.FontWeight.W_500)), on_click=lambda _: confirme(text.value)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(nome_arquivo)

    def arast(e, c):
        c.border = None

        datafix = e.src.content.data
        icon = e.src.content.data['icon']
        index = e.src.content.data['index']
        index_categoria_iten = None
        lista = {}
        try:
            index_categoria_iten = e.src.content.data['index_categoria']
        except:
            try:
                lista = e.src.content.data['lista']
            except:
                pass
            
        if not index_categoria_iten == None:
            iten = lista_dados[index_categoria_iten]['lista'].pop(index)
            lista_dados.append(iten)

            lista_visual.controls.clear()
            render()
        
    def accep(e, c):
        c.border = ft.Border.all(2, '#FBB100')
    def leave(e, c):
        c.border = None

    cont = ft.Container(
            expand=True,
            height=80,
            border_radius = 10,
            alignment=ft.Alignment.CENTER,
            content=ft.Text('Araste aqui para área externa.', size=10, weight=ft.FontWeight.BOLD, opacity=0.5, color='#FBB100')
        )
    
    cont_ =ft.Card(
            bgcolor="#362711",
            expand=True,
            height=80,
            content=cont
    )
    
    obrigatorio = ft.DragTarget(
                content=cont_,
                on_accept=lambda e, c=cont: arast(e, c),
                on_will_accept=lambda e, c=cont: accep(e, c),
                on_leave=lambda e, c=cont: leave(e, c),
            )

    lista_dados = dados
    lista_visual = ft.Column(
        spacing=0, 
        scroll=ft.ScrollMode.ALWAYS,
    )

    def on_drag_accept(e, c):
        nonlocal lista_dados
        on_leave(e, c)
        nome = e.src.content.data['nome']
        nome_original = c.data['nome']

        if not nome_original == nome:
            # RECEBIDO
            datafix = e.src.content.data
            icon = e.src.content.data['icon']
            index = e.src.content.data['index']
            index_categoria_iten = None
            lista = False
            try:
                index_categoria_iten = e.src.content.data['index_categoria']
            except:
                try:
                    lista = e.src.content.data['lista']
                except:
                    pass
            # CONTAINER QUE RECEBEU
            datafix_original = None
            icon_original = None
            index_original = None
            index_categoria = None
            lista_original = False

            try:
                datafix_original = c.data
                icon_original = c.data['icon']
                index_original = c.data['index']
                index_categoria = c.data['index_categoria']
            except:
                try:
                    lista_original = c.data['lista']
                except:
                    pass

            if not index_categoria == None:
                if index_categoria == index_categoria_iten:
                    iten_ = lista_dados[index_categoria]['lista'].pop(index)
                    lista_dados[index_categoria]['lista'].insert(index_original, iten_)

                    lista_visual.controls.clear()
                    render()
            else:
                if not index_categoria_iten == None and index_categoria == None:
                    iten__ = lista_dados[index_categoria_iten]['lista'].pop(index)
                    lista_dados[index_original]['lista'].append(iten__)
                    lista_visual.controls.clear()
                    render()
                else:
                    if lista_original == False:
                        try:
                            lista___ = lista_dados[index_original]['lista']
                            iten__ = lista_dados.pop(index)

                            lista___.append(iten__)
                            lista_visual.controls.clear()
                            render()
                        except Exception as e:
                            print(e)
                    else:
                        lista___ = lista_dados[index_original - 1]['lista']
                        iten__ = lista_dados.pop(index)

                        lista___.append(iten__)
                        lista_visual.controls.clear()
                        render()
                        

    def on_will_accept(container_alvo, c):
        nome = container_alvo.src.content.data['nome']
        nome_original = c.data['nome']

        if not nome_original == nome:
            categoria = None
            try: 
                index_categoria = c.data['index_categoria']
                categoria = True
            except:
                categoria = False
            if categoria:
                for elemento in c.content.controls:
                    elemento.color = ft.Colors.YELLOW
            else:
                for elemento in c.content.controls:
                    elemento.color = ft.Colors.YELLOW_200

    def on_leave(container_alvo, c):
        try:
            c.data['index_categoria']
            try:
                c.content.controls[0].color = None
                c.content.controls[1].color = '#FBB100'
                c.content.controls[2].color = None
            except:
                c.content.controls[0].color = '#FBB100'
                c.content.controls[1].color = None
        except:
            c.content.controls[0].color = '#FBB100'
            c.content.controls[1].color = None

    def Pasta(icon, nome, i):
        text = ft.Text(nome, size=25, weight=ft.FontWeight.BOLD)

        container1 = ft.Card(
            width=400,
            height=50,
            bgcolor='#402E15',
            data={'icon': icon, 'nome': nome, 'index': i},
            content=ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Icon(
                            icon=icon,
                            color="#DF9D04",
                            scale=1.6
                        ),
                        text,
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            scale=0.7,
                            on_click=chamar
                        ),
                    ]
                )
        )

        target_container = ft.Draggable(
                content=container1,
            
        )

        drag_target = ft.DragTarget(
            content=target_container,
            on_accept=lambda e, c=container1: on_drag_accept(e, c),
            on_will_accept=lambda e, c=container1: on_will_accept(e, c),
            on_leave=lambda e, c=container1: on_leave(e, c),
        )
        
        return drag_target
    def Arquivo(icon, nome, i_, i):
        icon_ = ft.Icon(
                        icon=icon,
                        color='#FBB100'
                    )
        text = ft.Text(
                    nome, 
                    size=15, 
                    weight=ft.FontWeight.BOLD
                )
        
        if icon == ft.Icons.FOLDER:
            icon_ = ft.Icon(
                    icon=icon,
                    color="#DF9D04"
                )
            
            text = ft.Text(
                        nome, 
                        size=15, 
                        weight=ft.FontWeight.BOLD,

                    )

        organiz = ft.Row(
                controls=[
                    icon_,
                    text
                ]
            )

        if not i == None:
            organiz = ft.Row(
                    controls=[
                        ft.VerticalDivider(
                            width=35
                        ),
                        icon_,
                        text
                    ]
                )
        

        container = ft.Container(
            width=400,
            height=25,
            data={'icon': icon, 'nome': nome, 'index': i_, 'index_categoria': i},
            content=organiz
        )

        container_opacity = ft.Card(
            bgcolor=ft.Colors.TRANSPARENT,
            width=400,
            height=50,
            content=ft.Row(
                controls=[
                    ft.Icon(
                        icon=icon,
                    ),
                    text
                ]
            ),
            opacity=0.5
        )

        target_container = ft.Draggable(
            content=container,
            content_feedback=container_opacity
        )

        drag_target = ft.DragTarget(
            content=target_container,
            on_accept=lambda e, c=container: on_drag_accept(e, c),
            on_will_accept=lambda e, c=container: on_will_accept(e, c),
            on_leave=lambda e, c=container: on_leave(e, c),
        )

        return drag_target
    def render():
        lista_visual.controls.append(obrigatorio)
        for i, iten in enumerate(lista_dados):
            icon = iten['icon']
            nome = iten['nome']
            try:
                lista = iten['lista']

                drag_target = Pasta(icon, nome, i)

                lista_visual.controls.append(drag_target)

                for i_, iten in enumerate(lista):
                    icon = iten['icon']
                    nome = iten['nome']
                    
                    drag_target2 = Arquivo(icon, nome, i_, i)
                    lista_visual.controls.append(drag_target2)
            except:
                drag_target = Arquivo(icon, nome, i, None)
                lista_visual.controls.append(drag_target)
        mudar(lista_dados)

    render()

    return lista_visual
