"""Работа с локальным тестовым графом."""

import json
import re
from pathlib import Path

PACKAGE_PATTERN = re.compile(r"^[A-Z]+$")


class TestRepositoryError(Exception):
    """Ошибка тестового репозитория."""


def validate_package(name):
    """Проверить имя тестового пакета."""
    return bool(PACKAGE_PATTERN.fullmatch(name))


def load_test_repository(path):
    """Загрузить и проверить граф из JSON-файла."""
    file_path = Path(path)
    try:
        text = file_path.read_text(encoding="utf-8")
        graph = json.loads(text)
    except (OSError, json.JSONDecodeError) as error:
        raise TestRepositoryError(
            "Не удалось прочитать тестовый репозиторий"
        ) from error

    validate_graph(graph)
    return graph


def _validate_dependencies(package, dependencies):
    """Проверить список зависимостей одного пакета."""
    if not isinstance(dependencies, list):
        raise TestRepositoryError(
            f"Зависимости {package} должны быть списком"
        )
    for dependency in dependencies:
        if not validate_package(dependency):
            raise TestRepositoryError(
                f"Некорректный пакет: {dependency}"
            )


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
        _validate_dependencies(package, dependencies)


class TestGraphBuilder:
    """Строитель тестового графа рекурсивным DFS."""

    def __init__(self, repository, max_depth):
        """Подготовить состояние обхода."""
        self.repository = repository
        self.max_depth = max_depth
        self.result = {}
        self.visited_depth = {}
        self.active = set()

    def build(self, start):
        """Построить граф от начального пакета."""
        if start not in self.repository:
            raise TestRepositoryError(
                f"Пакет {start} отсутствует в репозитории"
            )
        self._dfs(start, 0)
        return self.result

    def _should_skip(self, package, depth):
        """Проверить повторное посещение вершины."""
        previous = self.visited_depth.get(package)
        return previous is not None and previous <= depth

    def _dfs(self, package, depth):
        """Рекурсивно обойти одну тестовую вершину."""
        if self._should_skip(package, depth):
            return

        self.visited_depth[package] = depth
        self.result.setdefault(package, [])
        if depth >= self.max_depth:
            return

        self.active.add(package)
        self._visit_children(package, depth)
        self.active.remove(package)

    def _visit_children(self, package, depth):
        """Посетить зависимости текущего пакета."""
        for dependency in self.repository.get(package, []):
            if dependency not in self.result[package]:
                self.result[package].append(dependency)
            self.result.setdefault(dependency, [])
            if dependency not in self.active:
                self._dfs(dependency, depth + 1)


def build_test_graph(repository, start, max_depth):
    """Построить тестовый граф рекурсивным DFS."""
    builder = TestGraphBuilder(repository, max_depth)
    return builder.build(start)
