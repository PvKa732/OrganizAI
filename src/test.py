import flet as ft

def main(page: ft.Page):
    page.title = "Exemplo de Drag and Drop - Sem Texto"
    page.alignment = ft.Alignment.CENTER

    def on_drag_accept(e):
        src = page.get_control(e.src_id)
        cor_arrastada = src.content.bgcolor

        print(f"Cor do objeto: {cor_arrastada}")
        
        target_container.bgcolor = cor_arrastada
        target_container.border = None 
        page.update()

    def on_will_accept(e):
        target_container.border = ft.border.all(4, ft.Colors.GREEN)
        page.update()

    def on_leave(e):
        target_container.border = None
        page.update()
    # Cores dos 3 objetos
    cores = [ft.Colors.BLUE, ft.Colors.RED, ft.Colors.ORANGE]
    objetos_arrastaveis = []

    for cor in cores:
        draggable_item = ft.Draggable(
            group="quadrado",
            
            # 1. Objeto parado na tela (apenas o quadrado colorido, sem texto)
            content=ft.Container(
                width=100,
                height=100,
                bgcolor=cor,
                border_radius=5,
            ),
            
            # 2. Objeto sendo arrastado (vira uma bolinha colorida sem texto nem ícone)
            content_when_dragging=ft.Container(
                width=60,
                height=60,
                bgcolor=cor,
                border_radius=30,
                opacity=0.8,
            ),
            
            # 3. O espaço que fica para trás enquanto arrasta
            content_feedback=ft.Container(
                width=100,
                height=100,
                bgcolor=ft.Colors.GREEN,
                border_radius=5,
                opacity=0.5
            )
        )
        objetos_arrastaveis.append(draggable_item)

    # Alvo inicial (começa cinza e sem nenhuma borda por padrão)
    target_container = ft.Container(
        width=150,
        height=150,
        bgcolor=ft.Colors.GREY_300,
        border=None,
        border_radius=10,
        alignment=ft.Alignment.CENTER,
    )

    drag_target = ft.DragTarget(
        group="quadrado",
        content=target_container,
        on_accept=on_drag_accept,
        on_will_accept=on_will_accept,
        on_leave=on_leave,
    )

    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=objetos_arrastaveis, alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                ft.Row(controls=[drag_target], alignment=ft.MainAxisAlignment.CENTER)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)