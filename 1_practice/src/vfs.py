"""Модуль виртуальной файловой системы (VFS) в памяти."""

import os

DEFAULT_DIR_MODE = "755"
DEFAULT_FILE_MODE = "644"
ROOT_PATH = "/"


class VFSNode:
    """Узел виртуальной файловой системы."""

    def __init__(self, name, is_dir=False, content="", mode=None):
        """Инициализация узла файла или папки."""
        self.name = name
        self.is_dir = is_dir
        self.content = content
        default_m = DEFAULT_DIR_MODE if is_dir else DEFAULT_FILE_MODE
        self.mode = mode if mode else default_m
        self.children = {}


class VFS:
    """Класс управления виртуальной файловой системой в памяти."""

    def __init__(self):
        """Инициализация пустой VFS."""
        self.root = VFSNode("", is_dir=True)
        self.cwd = ROOT_PATH
        self.name = "empty"

    def load_from_dir(self, phys_path):
        """Загрузка структуры директории с диска в память."""
        if not os.path.exists(phys_path):
            raise FileNotFoundError(f"Путь '{phys_path}' не найден")
        if not os.path.isdir(phys_path):
            raise ValueError(f"Неверный формат: '{phys_path}' не директория")
        self.name = os.path.basename(os.path.abspath(phys_path))
        self.root = self._read_dir_recursive(phys_path, "")
        self.cwd = ROOT_PATH

    def _read_dir_recursive(self, current_phys, node_name):
        """Рекурсивное чтение папки в узлы памяти."""
        node = VFSNode(node_name, is_dir=True)
        for item in os.listdir(current_phys):
            full_p = os.path.join(current_phys, item)
            if os.path.isdir(full_p):
                node.children[item] = self._read_dir_recursive(full_p, item)
            elif os.path.isfile(full_p):
                node.children[item] = self._read_file_node(full_p, item)
        return node

    def _read_file_node(self, full_p, item):
        """Чтение содержимого файла в память."""
        try:
            with open(full_p, "r", encoding="utf-8") as file:
                text = file.read()
        except OSError:
            text = ""
        return VFSNode(item, is_dir=False, content=text)

    def resolve_path(self, path):
        """Преобразование относительного пути в абсолютный."""
        if path.startswith(ROOT_PATH):
            norm = os.path.normpath(path)
        else:
            norm = os.path.normpath(os.path.join(self.cwd, path))
        return norm.replace("\\", ROOT_PATH)

    def get_node(self, path):
        """Получение узла по пути в VFS."""
        abs_p = self.resolve_path(path)
        if abs_p == ROOT_PATH:
            return self.root
        parts = [p for p in abs_p.split(ROOT_PATH) if p]
        curr = self.root
        for part in parts:
            if not curr.is_dir or part not in curr.children:
                return None
            curr = curr.children[part]
        return curr

    def get_parent_and_name(self, path):
        """Получение родительского узла и имени целевого элемента."""
        abs_p = self.resolve_path(path)
        if abs_p == ROOT_PATH:
            return None, ""
        parent_p = os.path.dirname(abs_p).replace("\\", ROOT_PATH)
        base_name = os.path.basename(abs_p)
        return self.get_node(parent_p), base_name