"""Модуль реализации команд оболочки."""

from datetime import datetime

from vfs import VFSNode

EMPTY_COUNT = 0
ONE_ARG = 1
TWO_ARGS = 2
THREE_ARGS = 3
DEFAULT_HEAD_LINES = 10
MODE_LEN = 3
OCTAL_CHARS = "01234567"
LS_FLAGS = {"-l", "-a", "-la", "-al"}


def _split_ls_args(args):
    """Разделить аргументы ls на флаги и пути."""
    flags = [arg for arg in args if arg.startswith("-")]
    paths = [arg for arg in args if not arg.startswith("-")]
    return flags, paths


def _validate_ls_args(flags, paths):
    """Проверить аргументы команды ls."""
    if any(flag not in LS_FLAGS for flag in flags):
        return "Ошибка ls: неизвестный флаг\n"
    if len(paths) > ONE_ARG:
        return "Ошибка ls: слишком много аргументов\n"
    return None


def _format_file(node, long_format):
    """Сформировать строку для одного файла."""
    if long_format:
        return f"{node.mode} {node.name}\n"
    return f"{node.name}\n"


def exec_ls(vfs, args):
    """Вывести содержимое директории с флагами -l и -a."""
    flags, paths = _split_ls_args(args)
    error = _validate_ls_args(flags, paths)
    if error:
        return error

    long_format = any("l" in flag[1:] for flag in flags)
    show_all = any("a" in flag[1:] for flag in flags)
    target = paths[0] if paths else vfs.cwd
    node = vfs.get_node(target)

    if not node:
        return f"Ошибка ls: '{target}' не найден\n"
    if not node.is_dir:
        return _format_file(node, long_format)
    return _format_dir_children(node, long_format, show_all)


def _format_dir_children(node, long_format, show_all):
    """Сформировать список элементов директории."""
    lines = []
    for name, child in sorted(node.children.items()):
        line = _format_child(name, child, long_format, show_all)
        if line is not None:
            lines.append(line)
    return "\n".join(lines) + ("\n" if lines else "")


def _format_child(name, child, long_format, show_all):
    """Сформировать строку для дочернего элемента."""
    if name.startswith(".") and not show_all:
        return None
    suffix = "/" if child.is_dir else ""
    if long_format:
        return f"{child.mode} {name}{suffix}"
    return f"{name}{suffix}"


def exec_cd(vfs, args):
    """Сменить текущую директорию VFS."""
    if len(args) > ONE_ARG:
        return "Ошибка cd: слишком много аргументов\n"
    target = args[0] if args else "/"
    node = vfs.get_node(target)
    if not node:
        return f"Ошибка cd: директория '{target}' не найдена\n"
    if not node.is_dir:
        return f"Ошибка cd: '{target}' не является директорией\n"
    vfs.cwd = vfs.resolve_path(target)
    return ""


def exec_date(args):
    """Вывести текущую дату и время."""
    if len(args) > EMPTY_COUNT:
        return "Ошибка date: команда не принимает аргументов\n"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{now}\n"


def exec_head(vfs, args):
    """Вывести первые строки файла."""
    parsed = _parse_head_args(args)
    if isinstance(parsed, str):
        return parsed
    count, path = parsed
    node = vfs.get_node(path)
    if not node:
        return f"Ошибка head: файл '{path}' не найден\n"
    if node.is_dir:
        return f"Ошибка head: '{path}' является директорией\n"
    lines = node.content.splitlines()[:count]
    return "\n".join(lines) + ("\n" if lines else "")


def _parse_head_args(args):
    """Разобрать аргументы команды head."""
    if len(args) == ONE_ARG:
        return DEFAULT_HEAD_LINES, args[0]
    if len(args) == THREE_ARGS and args[0] == "-n":
        return _parse_head_count(args[1], args[2])
    return "Ошибка head: неверные аргументы\n"


def _parse_head_count(raw_count, path):
    """Проверить число строк команды head."""
    if not raw_count.isdigit():
        return "Ошибка head: число строк должно быть положительным числом\n"
    count = int(raw_count)
    if count <= EMPTY_COUNT:
        return "Ошибка head: число строк должно быть положительным числом\n"
    return count, path


def exec_touch(vfs, args):
    """Создать новый пустой файл в памяти VFS."""
    if len(args) != ONE_ARG:
        return "Ошибка touch: требуется ровно 1 аргумент (путь)\n"
    parent, name = vfs.get_parent_and_name(args[0])
    if not parent or not parent.is_dir:
        return (
            "Ошибка touch: родительская папка для "
            f"'{args[0]}' не найдена\n"
        )
    if not name:
        return "Ошибка touch: некорректное имя файла\n"
    if name not in parent.children:
        parent.children[name] = VFSNode(name, is_dir=False, content="")
    return ""


def exec_chmod(vfs, args):
    """Изменить права доступа к файлу или папке в памяти VFS."""
    if len(args) != TWO_ARGS:
        return "Ошибка chmod: требуется 2 аргумента (режим и путь)\n"
    mode, path = args
    if len(mode) != MODE_LEN:
        return f"Ошибка chmod: неверный формат прав '{mode}'\n"
    if not all(char in OCTAL_CHARS for char in mode):
        return f"Ошибка chmod: неверный формат прав '{mode}'\n"
    node = vfs.get_node(path)
    if not node:
        return f"Ошибка chmod: '{path}' не найден\n"
    node.mode = mode
    return ""
