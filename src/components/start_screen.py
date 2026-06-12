import flet as ft


class StartScreen(ft.Container):
    def __init__(self, on_select_device):
        super().__init__()

        btn_style = ft.ButtonStyle(
            side=ft.BorderSide(width=1, color="#a0cafd"),
            shape=ft.RoundedRectangleBorder(radius=10),
        )

        buttons = ft.Row(
            controls=[
                ft.Button(
                    content="Мониторы",
                    icon=ft.Icons.DESKTOP_WINDOWS_OUTLINED,
                    width=160,
                    height=80,
                    style=btn_style,
                    on_click=lambda _, d="desktop": on_select_device(d),
                ),
                ft.Button(
                    content="Планшеты",
                    icon=ft.Icons.TABLET,
                    width=160,
                    height=80,
                    style=btn_style,
                    on_click=lambda _, d="tablet": on_select_device(d),
                ),
                ft.Button(
                    content="Телефоны",
                    icon=ft.Icons.PHONE_IPHONE,
                    width=160,
                    height=80,
                    style=btn_style,
                    on_click=lambda _, d="phone": on_select_device(d),
                ),
                ft.Button(
                    content="Настройки",
                    icon=ft.Icons.SETTINGS,
                    width=160,
                    height=80,
                    style=btn_style,
                    on_click=lambda _, d="custom": on_select_device(d),
                ),
            ],
            wrap=True,
            spacing=10,
        )

        main_content = ft.Column(
            controls=[
                ft.Text("Выберите тип экрана", size=20,
                        weight=ft.FontWeight.BOLD),
                buttons,  # ваша переменная с кнопками
            ],
            spacing=50,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.expand = True
        self.padding = 16

        self.content = ft.Stack(
            controls=[
                main_content,
                ft.IconButton(
                    icon=ft.Icons.SUNNY,
                    top=0,
                    right=0,
                    on_click=self.change_theme
                )
            ]
        )

    def change_theme(self, e):
        current_mode = self.page.theme_mode
        if current_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        else:
            self.page.theme_mode = ft.ThemeMode.DARK
