"""Точка входа анализатора зависимостей."""

from config import parse_config
from graph_builder import build_npm_graph
from npm_client import NpmClientError
from reverse_dependencies import find_reverse_dependencies
from test_repository import (
    TestRepositoryError,
    build_test_graph,
    load_test_repository
)


def print_graph(graph):
    """Вывести граф в виде списка смежности."""

    print()
    print("Граф зависимостей:")

    for package in sorted(graph):
        dependencies = graph[package]

        if dependencies:
            text = ", ".join(
                sorted(dependencies)
            )
        else:
            text = "нет зависимостей"

        print(
            f"{package} -> {text}"
        )


def print_reverse_dependencies(
    package,
    dependencies
):
    """Вывести обратные зависимости."""

    print()
    print(
        f"Обратные зависимости пакета {package}:"
    )

    if not dependencies:
        print("Нет обратных зависимостей")
        return

    for dependency in dependencies:
        print(
            f"- {dependency}"
        )


def run_test_mode(config):
    """Запустить программу с тестовым репозиторием."""

    repository = load_test_repository(
        config.repository
    )

    # Сначала строим обычный граф пакета.
    graph = build_test_graph(
        repository,
        config.package,
        config.max_depth
    )

    print_graph(graph)

    # Затем ищем пакеты, которые зависят
    # от указанного пользователем пакета.
    reverse = find_reverse_dependencies(
        repository,
        config.package,
        config.max_depth
    )

    print_reverse_dependencies(
        config.package,
        reverse
    )


def run_npm_mode(config):
    """Построить реальный граф npm."""

    graph, versions = build_npm_graph(
        config.repository,
        config.package,
        config.version,
        config.max_depth
    )

    print_graph(graph)

    print()
    print("Выбранные версии:")

    for package in sorted(versions):
        print(
            f"{package}: {versions[package]}"
        )


def main():
    """Запустить приложение."""

    config = parse_config()

    try:
        if config.test_mode:
            run_test_mode(config)
        else:
            run_npm_mode(config)

    except (
        NpmClientError,
        TestRepositoryError
    ) as error:
        print(
            f"Ошибка: {error}"
        )

        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())