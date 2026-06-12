import flet as ft
from components import SidePanel
from controllers import ContentArea
from utils import logs
import pathlib


def main(page: ft.Page):
    icon_path = pathlib.Path(__file__).parent / "src" / "assets" / "icon.png"
    page.window.icon = str(icon_path)

    page.title = "WebSize"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0

    def on_bookmark_click(bookmark_id):
        if main_content_area:
            main_content_area.open_bookmark(bookmark_id)

    def on_bookmark_delete(bookmark_id):
        if main_content_area:
            side_panel.remove_bookmark(bookmark_id)
            main_content_area.remove_bookmark(bookmark_id)

    def on_update_bookmark(bookmark_id, bookmark_data):
        """Обновляет закладку в панели (например, название)"""
        side_panel.update_bookmark_state(bookmark_id, bookmark_data)

    side_panel = SidePanel(
        on_go_home=lambda: main_content_area.show_start_screen() if main_content_area else None,
        on_bookmark_click=on_bookmark_click,
        on_bookmark_delete=on_bookmark_delete
    )

    main_content_area = ContentArea(
        page, side_panel.add_bookmark, on_update_bookmark)

    page.add(
        ft.Row(
            controls=[side_panel, main_content_area],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )

    page.window.min_width = 1100
    page.window.min_height = 600
    page.window.resizable = True

    page.update()


if __name__ == "__main__":
    logs()
    ft.run(main)
