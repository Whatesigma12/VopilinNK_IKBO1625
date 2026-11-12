"""Работа с локальным тестовым графом."""

import json
import re

from pathlib import Path


PACKAGE_PATTERN = re.compile(r"^[A-Z]+$")


class TestRepositoryError(Exception):
    """Ошибка тестового репозитория."""


def validate_package(name):
    """Проверить имя тестового пакета."""

    return bool(
        PACKAGE_PATTERN.fullmatch(name)
    )


def load_test_repository(path):
    """Загрузить граф из JSON-файла."""

    file_path = Path(path)

    try:
        text = file_path.read_text(
            encoding="utf-8"
        )
        graph = json.loads(text)
    except (OSError, json.JSONDecodeError) as error:
        raise TestRepositoryError(
            "Не удалось прочитать тестовый репозиторий"
        ) from error

    validate_graph(graph)

    return graph


def validate_graph(graph):
    """Проверить формат тестового графа."""

    if not isinstance(graph, dict):
        raise TestRepositoryError(
            "Корнем графа должен быть объект JSON"
        )

    for package, dependencies in graph.items():
        if not validate_package(package):
            raise TestRepositoryError(
                f"Некорректный пакет: {package}"
            )

        if not isinstance(dependencies, list):
            raise TestRepositoryError(
                f"Зависимости {package} должны быть списком"
            )

        for dependency in dependencies:
            if not validate_package(dependency):
                raise TestRepositoryError(
                    f"Некорректный пакет: {dependency}"
                )


def build_test_graph(repository, start, max_depth):
    """Построить тестовый граф рекурсивным DFS."""

    result = {}
    visited_depth = {}
    active = set()

    def dfs(package, depth):
        """Рекурсивно обойти одну тестовую вершину."""

        previous = visited_depth.get(package)

        if previous is not None and previous <= depth:
            return

        visited_depth[package] = depth
        result.setdefault(package, [])

        if depth >= max_depth:
            return

        active.add(package)

        for dependency in repository.get(package, []):
            if dependency not in result[package]:
                result[package].append(dependency)

            result.setdefault(dependency, [])

            if dependency not in active:
                dfs(
                    dependency,
                    depth + 1
                )

        active.remove(package)

    if start not in repository:
        raise TestRepositoryError(
            f"Пакет {start} отсутствует в репозитории"
        )

    dfs(start, 0)

    return result