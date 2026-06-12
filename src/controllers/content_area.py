import flet as ft
import uuid
from components.device_screen import DeviceScreen
from components.start_screen import StartScreen


class ContentArea(ft.Container):
    def __init__(self, main_page: ft.Page, on_add_bookmark, on_update_bookmark):
        super().__init__()
        self.expand = True
        self.main_page = main_page
        self.on_add_bookmark = on_add_bookmark
        self.on_update_bookmark = on_update_bookmark

        self.start_screen = StartScreen(
            on_select_device=self.show_device_screen)

        self.current_screen = ft.Container(
            expand=True,
            content=self.start_screen,
        )

        self.content = self.current_screen
        self.bookmarks = {}

    def show_device_screen(self, device_type: str, saved_state=None):
        if saved_state:
            screen = DeviceScreen(
                device_type=saved_state["type"],
                main_page=self.main_page,
                px_value=saved_state["px_value"],
                window_width=saved_state.get("window_width"),
                window_height=saved_state.get("window_height"),
                bookmark_id=saved_state["id"],
                on_save_callback=self.save_bookmark,
                on_close_callback=self.on_device_close
            )
        else:
            new_id = str(uuid.uuid4())
            screen = DeviceScreen(
                device_type,
                self.main_page,
                100,
                bookmark_id=new_id,
                on_save_callback=self.save_bookmark,
                on_close_callback=self.on_device_close
            )

        self.current_screen.content = screen
        self.current_screen.update()

    def save_bookmark(self, bookmark_data):
        bookmark_id = bookmark_data["id"]
        if bookmark_id not in self.bookmarks:
            self.bookmarks[bookmark_id] = bookmark_data
            self.on_add_bookmark(
                bookmark_id, bookmark_data["name"], bookmark_data["icon"])
        else:
            self.bookmarks[bookmark_id] = bookmark_data
            self.on_update_bookmark(bookmark_id, bookmark_data)

    def on_device_close(self, bookmark_id, bookmark_data):
        if bookmark_id and bookmark_data:
            self.save_bookmark(bookmark_data)

    def show_start_screen(self):
        current_screen = self.current_screen.content
        if isinstance(current_screen, DeviceScreen):
            bookmark_data = current_screen.get_current_state()
            self.save_bookmark(bookmark_data)

        self.current_screen.content = self.start_screen
        self.current_screen.update()

    def remove_bookmark(self, bookmark_id):
        if bookmark_id in self.bookmarks:
            del self.bookmarks[bookmark_id]

    def open_bookmark(self, bookmark_id):
        current_screen = self.current_screen.content
        if isinstance(current_screen, DeviceScreen):
            bookmark_data = current_screen.get_current_state()
            self.save_bookmark(bookmark_data)

        if bookmark_id in self.bookmarks:
            self.show_device_screen(
                None, saved_state=self.bookmarks[bookmark_id])
