import flet as ft
import uuid
import pyperclip


class DeviceScreen(ft.Container):
    """Окно калькулятора"""
    DEVICE_INFO = {
        "desktop": ("Мониторы", ft.Icons.DESKTOP_WINDOWS_OUTLINED, 1920, 1080),
        "tablet": ("Планшеты", ft.Icons.TABLET, 772, 926),
        "phone": ("Телефоны", ft.Icons.PHONE_IPHONE, 374, 812),
        "custom": ("Настройки", ft.Icons.SETTINGS, 1920, 1080),
    }

    SIZE_BUTTON = [
        "width", "height", "margin-left", "margin-top", "margin-right",
        "margin-bottom", "padding-left", "padding-top", "padding-right",
        "padding-bottom", "left", "top", "border-radius", "font-size"
    ]

    def __init__(self, device_type: str, main_page: ft.Page = None, px_value: float = 100,
                 window_width=None, window_height=None, bookmark_id=None,
                 on_save_callback=None, on_close_callback=None):
        super().__init__()

        self.main_page = main_page
        self.device_type = device_type
        self.px_value = px_value
        self.bookmark_id = bookmark_id
        self.on_save_callback = on_save_callback
        self.on_close_callback = on_close_callback

        title, icon, default_width, default_height = self.DEVICE_INFO.get(
            device_type, ("Неизвестно", ft.Icons.HELP, 1920, 1080))

        self.width_window = window_width if window_width else default_width
        self.height_window = window_height if window_height else default_height

        self.inputSizePX = ft.TextField(
            label="Введите размер в px",
            width=300,
            value=str(px_value),
            on_change=self.auto_save
        )

        self.inputSizeWindow = ft.TextField(
            label="Размер окна (ширина x высота)",
            width=300,
            value=f"{self.width_window}x{self.height_window}",
            on_change=self.auto_save
        ) if device_type == "custom" else None

        self.buttons_container = ft.Container(
            content=self.create_result_buttons(),
            padding=10
        )

        input_controls = [self.inputSizePX]
        if self.inputSizeWindow:
            input_controls.append(self.inputSizeWindow)

        self.expand = True
        self.padding = 16
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon, size=32, color="#a0cafd"),
                        ft.Text(title, size=28, weight=ft.FontWeight.BOLD)
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=input_controls,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                self.buttons_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )

    def get_current_state(self):
        return {
            "id": self.bookmark_id if self.bookmark_id else str(uuid.uuid4()),
            "name": self.DEVICE_INFO[self.device_type][0],
            "type": self.device_type,
            "icon": self.DEVICE_INFO[self.device_type][1],
            "px_value": float(self.inputSizePX.value),
            "window_width": self.width_window,
            "window_height": self.height_window,
        }

    def auto_save(self, e=None):
        try:
            self.px_value = float(self.inputSizePX.value)
        except (ValueError, TypeError):
            return

        if self.device_type == "custom" and self.inputSizeWindow and self.inputSizeWindow.value:
            try:
                if 'x' in self.inputSizeWindow.value:
                    w, h = self.inputSizeWindow.value.split('x')
                    self.width_window = float(w.strip())
                    self.height_window = float(h.strip())
                else:
                    self.width_window = float(self.inputSizeWindow.value)
                    self.height_window = float(self.inputSizeWindow.value)
            except (ValueError, TypeError):
                pass

        self.buttons_container.content = self.create_result_buttons()

        if self.on_save_callback:
            bookmark_data = self.get_current_state()
            self.on_save_callback(bookmark_data)

        self.update()

    def create_result_buttons(self):
        if self.width_window > 0 and self.height_window > 0:
            px_to_vw = round((self.px_value / self.width_window) * 100, 4)
            px_to_vh = round((self.px_value / self.height_window) * 100, 4)
        else:
            px_to_vw = px_to_vh = 0

        vw_props = {"width", "margin-left", "margin-right",
                    "padding-left", "padding-right", "left"}
        vh_props = {"height", "margin-top", "margin-bottom",
                    "padding-top", "padding-bottom", "top"}
        vmin_props = {"border-radius", "font-size"}

        btn_style = ft.ButtonStyle(
            side=ft.BorderSide(width=1, color="#a0cafd"),
            shape=ft.RoundedRectangleBorder(radius=10),
        )

        rows = []
        for key in self.SIZE_BUTTON:
            if key in vw_props:
                value = f"{px_to_vw}vw"
                buildValue = f"{key}: {px_to_vw}vw;"
            elif key in vh_props:
                value = f"{px_to_vh}vh"
                buildValue = f"{key}: {px_to_vh}vh;"
            elif key in vmin_props:
                value = f"{px_to_vw}vw/{px_to_vh}vh"
                buildValue = f"{key}: min({px_to_vw}vw, {px_to_vh}vh);"
            else:
                value = f"{px_to_vw}vw"
                buildValue = f"{key}: {px_to_vw}vw;"

            row = ft.Row(
                controls=[
                    ft.Text(value=key, width=100, size=12),
                    ft.TextButton(
                        content=ft.Text(
                            value, size=12, weight=ft.FontWeight.BOLD),
                        width=160,
                        height=30,
                        style=btn_style,
                        on_click=lambda _, v=value: self.copy_to_clipboard(v),
                    ),
                    ft.TextButton(
                        content=ft.Text("Copy", size=12,
                                        weight=ft.FontWeight.BOLD),
                        width=55,
                        height=30,
                        style=btn_style,
                        on_click=lambda _, v=buildValue: self.copy_to_clipboard(
                            v),
                    ),
                ],
                width=330,
                spacing=1,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            rows.append(row)

        columns = [
            ft.Column(controls=rows[i: i+7])
            for i in range(0, len(rows), 7)
        ]

        return ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=columns,
            spacing=5,
        )

    def copy_to_clipboard(self, value):
        if self.main_page:
            pyperclip.copy(value)
