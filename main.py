import sys
from pathlib import Path

# Добавляем src в путь поиска
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Импортируем и запускаем твой реальный main из src
from main import main

if __name__ == "__main__":
    import flet as ft
    ft.app(target=main)
