import json
from math import ceil
from typing import Any, Union


class Menu_bot_settings:
    def __init__(self, opening_lines: list[str], main_menu_name: str, items_list: list):
        self._opening_lines = opening_lines # Для рендера текста перед меню
        self._main_menu_name = main_menu_name # Для объявления имени главного меню
        self._items_list = items_list

        # Навигационные состояния
        self._path = [] # Хранит путь до текущего подменю в формате [Имя, лист]
        self._cursor = 0 # Индекс выбранного пункта на странице
        self._page = 0 # Номер текущей страницы
        self._items_per_page = 5 # Количество пунктов на одной странице

    def _get_current_items_list(self) -> list: # Возвращает список элементов в соответствии с path
        if self._path:
            current = self._path[-1][1]
        else:
            current = self._items_list
        return current
    
    def _get_current_page(self) -> list:
        start = self._page * self._items_per_page
        end = start + self._items_per_page
        return self._get_current_items_list()[start:end]
    
    def get_current_item(self):
        current_page = self._get_current_page()
        current_item = current_page[self._cursor]
        return current_item

    def move_cursor(self, d: int) -> None:
        current_page = self._get_current_page()
        if 0 > self._cursor + d:
            self._cursor = len(current_page)-1
        elif self._cursor + d > len(current_page)-1:
            self._cursor = 0
        else:
            self._cursor += d
                    
    def change_page(self, d: int) -> None:
        num_of_pages = ceil(len(self._get_current_items_list()) / self._items_per_page)
        if 0 > self._page + d:
            self._page = num_of_pages-1
            self._cursor = 0
        elif self._page + d > num_of_pages-1:
            self._page = 0
            self._cursor = 0
        else:
            self._page += d
            self._cursor = 0

    def enter(self, input_data: Any = None) -> str:
        current_page = self._get_current_page()
        current_item = current_page[self._cursor]
        
        match current_item[0]:
            case "note":
                return
            case "switch":
                current_item[2] = not current_item[2]
                return
            case "text":
                if isinstance(input_data, str):
                    current_item[2] = input_data
                return
            case "chooseable":
                if isinstance(input_data, int):
                    current_item[2] = input_data
                return
            case "menu":
                self._path.append([current_item[1], current_item[2]])
                self._page = 0
                self._cursor = 0
                return
            case _:
                return

    def back(self) -> None:
        if self._path:
            self._path.pop()
            self._cursor = 0
            self._page = 0

    def export_menu(self) -> str:
        return json.dumps(self._items_list)

    def import_menu(self, data: str) -> None:
        self._items_list = json.loads(data)
        self.path = []
        self.cursor = 0
        self.page = 0

    def render(self) -> str:
        lines = list(self._opening_lines)

        if self._path:
            lines.append("## "+self._path[-1][0])
        elif self._main_menu_name:
            lines.append(self._main_menu_name)
        else:
            lines.append("## Главное меню")
            
        lines.append("```")
        current_page = self._get_current_page()
        for idx, current_item in enumerate(current_page):
            is_selected = idx == self._cursor
            pointer = "→" if is_selected else " "
            
            match current_item[0]:
                case "note":
                    lines.append(f"{pointer} {current_item[1]}")
                case "switch":
                    lines.append(f"{pointer} ● {current_item[1]}\n  └─► {current_item[2]}")
                case "text":
                    lines.append(f"{pointer} ● {current_item[1]}\n  └─► {current_item[2]}")
                case "chooseable":
                    lines.append(f"{pointer} ● {current_item[1]}\n  └─► {current_item[3][current_item[2]]}")
                case "menu":
                    lines.append(f"{pointer} ≡ {current_item[1]}")
                case _:
                    continue
        
        num_of_pages = ceil(len(self._get_current_items_list()) / self._items_per_page)
        lines.append(f"\nСтраница {self._page+1}/{num_of_pages}")

        lines.append("```")

        return "\n".join(lines)
