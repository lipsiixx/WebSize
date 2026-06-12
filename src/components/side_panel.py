import flet as ft


class SidePanel(ft.Container):
    def __init__(self, on_go_home, on_bookmark_click, on_bookmark_delete):
        super().__init__()

        self.on_bookmark_click = on_bookmark_click
        self.on_bookmark_delete = on_bookmark_delete

        self.btn_home = ft.TextButton(
            content="Домой",
            icon=ft.Icons.MAPS_HOME_WORK_ROUNDED,
            width=250,
            on_click=lambda _: on_go_home(),
            style=ft.ButtonStyle(
                side=ft.BorderSide(width=1, color="#a0cafd"),
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        )

        self.bookmarks_container = ft.Column(spacing=8)

        self.width = 250
        self.border_radius = 20
        self.margin = 5
        self.padding = 15

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.btn_home,
                    ft.Divider(height=20, color="#a0cafd"),
                    self.bookmarks_container,
                ],
                tight=True,
                spacing=10,
            ),
            width=220,
            height=120,
            border=ft.Border.all(1, ft.Colors.BLUE_200),
            border_radius=10,
            padding=16,
        )

    def add_bookmark(self, bookmark_id, name, icon):
        for control in self.bookmarks_container.controls:
            if hasattr(control, 'bookmark_id') and control.bookmark_id == bookmark_id:
                return

        bookmark_row = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=icon,
                        icon_size=20,
                        on_click=lambda _, bid=bookmark_id: self.on_bookmark_click(
                            bid),
                        tooltip=name,
                    ),
                    ft.TextButton(
                        content=name,
                        on_click=lambda _, bid=bookmark_id: self.on_bookmark_click(
                            bid),
                        style=ft.ButtonStyle(padding=0),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_size=16,
                        icon_color="red",
                        on_click=lambda _, bid=bookmark_id: self.on_bookmark_delete(
                            bid),
                        tooltip="Удалить",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=5,
            ),
            padding=5,
            border_radius=8,
        )
        print(1)
        bookmark_row.bookmark_id = bookmark_id
        self.bookmarks_container.controls.append(bookmark_row)
        self.update()

    def update_bookmark_state(self, bookmark_id, bookmark_data):
        for control in self.bookmarks_container.controls:
            if hasattr(control, 'bookmark_id') and control.bookmark_id == bookmark_id:
                for row_control in control.content.controls:
                    if isinstance(row_control, ft.TextButton):
                        row_control.text = bookmark_data.get(
                            "name", row_control.content)
                self.update()
                break

    def remove_bookmark(self, bookmark_id):
        for i, control in enumerate(self.bookmarks_container.controls):
            if hasattr(control, 'bookmark_id') and control.bookmark_id == bookmark_id:
                self.bookmarks_container.controls.pop(i)
                self.update()
                break
