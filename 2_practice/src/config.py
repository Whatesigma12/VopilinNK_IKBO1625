"""Разбор и проверка параметров командной строки."""

import argparse
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_MAX_DEPTH = 3
MIN_DEPTH = 0
HTTP_SCHEMES = ("http", "https")


@dataclass
class Config:
    """Настройки анализатора зависимостей."""

    package: str
    repository: str
    test_mode: bool
    version: str
    max_depth: int


def positive_depth(value):
    """Преобразовать глубину в неотрицательное целое число."""
    try:
        depth = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "Глубина должна быть целым числом"
        ) from error

    if depth < MIN_DEPTH:
        raise argparse.ArgumentTypeError(
            "Глубина не может быть отрицательной"
        )
    return depth


def build_parser():
    """Создать парсер параметров командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализатор зависимостей npm, вариант 8"
    )
    parser.add_argument(
        "--package",
        required=True,
        help="Название анализируемого пакета",
    )
    parser.add_argument(
        "--repository",
        required=True,
        help="URL npm-реестра или путь к тестовому файлу",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Использовать локальный тестовый репозиторий",
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Версия анализируемого пакета",
    )
    parser.add_argument(
        "--max-depth",
        type=positive_depth,
        default=DEFAULT_MAX_DEPTH,
        help="Максимальная глубина обхода графа",
    )
    return parser


def _clean_values(options):
    """Очистить текстовые параметры от внешних пробелов."""
    return (
        options.package.strip(),
        options.repository.strip(),
        options.version.strip(),
    )


def _validate_required(parser, package, repository, version):
    """Проверить обязательные текстовые параметры."""
    if not package:
        parser.error("Название пакета не может быть пустым")
    if not repository:
        parser.error("Репозиторий не может быть пустым")
    if not version:
        parser.error("Версия пакета не может быть пустой")


def _validate_test_mode(parser, package, repository):
    """Проверить параметры тестового режима."""
    if not Path(repository).is_file():
        parser.error("Тестовый файл не найден")
    valid_name = (
        package.isascii()
        and package.isalpha()
        and package.isupper()
    )
    if not valid_name:
        parser.error(
            "В тестовом режиме имя пакета должно состоять из A-Z"
        )


def _validate_url(parser, repository):
    """Проверить URL реального репозитория."""
    parsed = urlparse(repository)
    if parsed.scheme not in HTTP_SCHEMES or not parsed.netloc:
        parser.error("Укажите корректный HTTP(S) URL репозитория")


def parse_config(args=None):
    """Прочитать, проверить и вернуть параметры программы."""
    parser = build_parser()
    options = parser.parse_args(args)
    package, repository, version = _clean_values(options)
    _validate_required(parser, package, repository, version)

    if options.test_mode:
        _validate_test_mode(parser, package, repository)
    else:
        _validate_url(parser, repository)

    return Config(
        package=package,
        repository=repository,
        test_mode=options.test_mode,
        version=version,
        max_depth=options.max_depth,
    )
