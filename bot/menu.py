import json


class Menu:

    def __init__(self, opening_lines: list, main_menu_name: str, items_map: dict | None):
        self.opening_lines = opening_lines
        self.main_menu_name = main_menu_name
        # Глубокое копирование через JSON для поддержки функции cancel()
        self._initial_map = json.dumps(items_map)
        self.items_map = items_map if items_map is not None else {}

        # Навигационные состояния
        self.path = []  # Хранит путь до текущего подменю
        self.cursor = 0  # Индекс выбранного пункта на текущей странице
        self.page = 0  # Номер текущей страницы
        self.items_per_page = 5

    def _get_current_menu(self) -> dict:
        """Возвращает словарь текущего уровня меню."""
        current = self.items_map
        for step in self.path:
            current = current[step]
        return current if isinstance(current, dict) else {}

    def _get_current_items(self) -> list:
        """Возвращает список элементов (ключ, значение) текущего уровня."""
        return list(self._get_current_menu().items())

    def render(self) -> str:
        """Выводит меню в текстовом формате с учетом страниц и курсора."""
        lines = list(self.opening_lines)

        # Добавляем хлебные крошки (название текущего подменю)
        if self.path:
            lines.append("## "+self.path[-1])
        elif self.main_menu_name:
            lines.append(self.main_menu_name)
        else:
            lines.append("## Главное меню")

        items = self._get_current_items()
        if not items:
            return "\n".join(lines)

        # Пагинация
        start = self.page * self.items_per_page
        end = start + self.items_per_page
        page_items = items[start:end]

        for idx, (key, val) in enumerate(page_items):
            # Проверяем, совпадает ли глобальный индекс с курсором
            is_selected = (start + idx) == self.cursor
            pointer = "► " if is_selected else ""

            if isinstance(val, dict):
                lines.append(f"{pointer}`≡ {key}`")
            elif isinstance(val, bool):
                status = "`Да`" if val else "`Нет`"
                lines.append(f"{pointer}`● {key}` -> {status}")
            elif isinstance(val, str):
                lines.append(f"{pointer}`■ {key}` -> `{val}`")
            elif callable(val):
                lines.append(f"{pointer}`► {key}`")
            elif val is None:
                lines.append(f"{pointer}{key}")

        return "\n".join(lines)

    def enter(self) -> None:
        """Выполняет действие над выбранным пунктом меню."""
        items = self._get_current_items()
        if not items:
            return

        key, val = items[self.cursor]

        if isinstance(val, dict):
            # Переход во вложенное меню
            self.path.append(key)
            self.cursor = 0
            self.page = 0
        elif isinstance(val, bool):
            # Переключение булева значения
            current_menu = self._get_current_menu()
            current_menu[key] = not val
        elif isinstance(val, str):
            # Редактирование текста
            ...
        elif callable(val):
            # Вызов функции
            val()
        elif val is None:
            # Ничего не происходит
            pass

    def back(self) -> None:
        """Возвращает из подменю обратно в родительское меню."""
        if self.path:
            self.path.pop()
            self.cursor = 0
            self.page = 0

    def next_page(self) -> None:
        """Перемещает курсор вниз или переключает на следующую страницу."""
        items = self._get_current_items()
        total_items = len(items)

        if total_items == 0:
            return

        # Сдвигаем курсор
        self.cursor = (self.cursor + 1) % total_items
        # Рассчитываем страницу на основе курсора
        self.page = self.cursor // self.items_per_page

    def prev_page(self) -> None:
        """Перемещает курсор вверх или переключает на предыдущую страницу."""
        items = self._get_current_items()
        total_items = len(items)

        if total_items == 0:
            return

        # Сдвигаем курсор назад
        self.cursor = (self.cursor - 1) % total_items
        self.page = self.cursor // self.items_per_page

    def save(self) -> None:
        """Сохраняет сделанные изменения."""
        ...

    def cancel(self) -> None:
        """Отменяет все изменения, возвращая меню к исходному состоянию."""
        ...

    def export_menu(self) -> str:
        """Экспортирует карту пунктов в строку JSON для хранения в SQLite."""
        # Функции (callable) нельзя сериализовать в JSON напрямую.
        # Для демонстрации они временно заменяются строковой меткой.
        def clean_map(d):
            if not isinstance(d, dict):
                return d
            return {
                k: (
                    v.__name__
                    if callable(v)
                    else (clean_map(v) if isinstance(v, dict) else v)
                )
                for k, v in d.items()
            }

        return json.dumps(clean_map(self.items_map), ensure_ascii=False)

    def import_menu(self, text_data: str) -> None:
        """Импортирует карту пунктов из строки JSON."""
        self.items_map = json.loads(text_data)
        self.path = []
        self.cursor = 0
        self.page = 0
