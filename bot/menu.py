import json


class Menu:

    def __init__(self, opening_lines: list, main_menu_name: str, items_map: dict | None):
        self.opening_lines = opening_lines # Для рендера текста перед меню
        self.main_menu_name = main_menu_name # Для объявления имени главного меню
        
        self._initial_map = json.dumps(items_map)
        self.items_map = items_map if items_map is not None else {}

        # Навигационные состояния
        self.path = [] # Хранит путь до текущего подменю
        self.cursor = 0 # Индекс выбранного пункта на текущей странице
        self.page = 0 # Номер текущей страницы
        self.items_per_page = 5 # Количество пунктов на одной странице

    def _get_current_menu(self) -> dict:
        current = self.items_map
        for step in self.path:
            current = current[step]
        return current if isinstance(current, dict) else {}

    def _get_current_items(self) -> list:
        return list(self._get_current_menu().items())

    def render(self) -> str:
        lines = list(self.opening_lines)

        if self.path:
            lines.append("## "+self.path[-1])
        elif self.main_menu_name:
            lines.append(self.main_menu_name)
        else:
            lines.append("## Главное меню")

        items = self._get_current_items()
        if not items:
            return "\n".join(lines)

        start = self.page * self.items_per_page
        end = start + self.items_per_page
        page_items = items[start:end]
        
        lines.append("```")

        for idx, (key, val) in enumerate(page_items):
            is_selected = (start + idx) == self.cursor
            pointer = "►" if is_selected else " "

            if isinstance(val, dict):
                lines.append(f"{pointer} ≡ {key}")
            elif isinstance(val, bool):
                status = "True" if val else "False"
                lines.append(f"{pointer} ● {key}\n    → {status}") # Пробелы сделаны для красоты, табуляция в monospace дискорда.
            elif isinstance(val, list):
                lines.append(f"{pointer} ● {key}\n    → {val[val[0]]}") # АААААААААААААА, УБЕРИТЕ ЭТО!
            elif isinstance(val, str):
                lines.append(f"{pointer} ■ {key}\n    → {val}")
            elif callable(val):
                lines.append(f"{pointer} ► {key}")
            elif val is None:
                lines.append(f"{pointer} {key}")

        lines.append("```")

        return "\n".join(lines)

    def enter(self) -> None:
        items = self._get_current_items()
        if not items:
            return

        key, val = items[self.cursor]

        if isinstance(val, dict):
            self.path.append(key)
            self.cursor = 0
            self.page = 0
        elif isinstance(val, bool):
            current_menu = self._get_current_menu()
            current_menu[key] = not val
        elif isinstance(val, list):
            ...  # TODO
        elif isinstance(val, str):
            ...  # TODO
        elif val is None:
            pass

    def back(self) -> None:
        if self.path:
            self.path.pop()
            self.cursor = 0
            self.page = 0

    def next_page(self) -> None:
        items = self._get_current_items()
        total_items = len(items)

        if total_items == 0:
            return

        self.cursor = (self.cursor + 1) % total_items
        self.page = self.cursor // self.items_per_page

    def prev_page(self) -> None:
        items = self._get_current_items()
        total_items = len(items)

        if total_items == 0:
            return

        self.cursor = (self.cursor - 1) % total_items
        self.page = self.cursor // self.items_per_page

    def save(self) -> None:
        ... # TODO

    def cancel(self) -> None:
        ... # TODO

    def export_menu(self) -> str:
        ... # TODO

    def import_menu(self, text_data: str) -> None:
        self.items_map = json.loads(text_data)
        self.path = []
        self.cursor = 0
        self.page = 0
