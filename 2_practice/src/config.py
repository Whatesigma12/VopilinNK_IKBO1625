
import argparse
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


# Храним настройки программы в одном объекте.
@dataclass
class Config:
    package: str
    repository: str
    test_mode: bool
    version: str
    max_depth: int


def positive_depth(value):
    """Проверяем, что глубина — целое число от нуля."""

    try:
        depth = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Глубина должна быть целым числом"
        )

    if depth < 0:
        raise argparse.ArgumentTypeError(
            "Глубина не может быть отрицательной"
        )

    return depth


def parse_config(args=None):
    """Читаем и проверяем параметры командной строки."""

    parser = argparse.ArgumentParser(
        description="Анализатор зависимостей npm, вариант 8"
    )

    parser.add_argument(
        "--package",
        required=True,
        help="Название анализируемого пакета"
    )

    parser.add_argument(
        "--repository",
        required=True,
        help="URL npm-реестра или путь к тестовому файлу"
    )

    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Использовать локальный тестовый репозиторий"
    )

    parser.add_argument(
        "--version",
        required=True,
        help="Версия анализируемого пакета"
    )

    parser.add_argument(
        "--max-depth",
        type=positive_depth,
        default=3,
        help="Максимальная глубина обхода графа"
    )

    options = parser.parse_args(args)

    # Убираем пробелы вокруг текстовых параметров.
    package = options.package.strip()
    repository = options.repository.strip()
    version = options.version.strip()

    if not package:
        parser.error("Название пакета не может быть пустым")

    if not version:
        parser.error("Версия пакета не может быть пустой")

    if not repository:
        parser.error("Репозиторий не может быть пустым")

    if options.test_mode:
        # В тестовом режиме нужен существующий файл.
        if not Path(repository).is_file():
            parser.error("Тестовый файл не найден")

        # По заданию тестовые пакеты — большие латинские буквы.
        if not package.isascii() or not package.isalpha() or not package.isupper():
            parser.error("В тестовом режиме имя пакета должно состоять из A-Z")

    else:
        # В обычном режиме нужен корректный HTTP(S) URL.
        parsed = urlparse(repository)

        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            parser.error("Укажите корректный HTTP(S) URL репозитория")

    return Config(
        package=package,
        repository=repository,
        test_mode=options.test_mode,
        version=version,
        max_depth=options.max_depth
    )
