"""Точка входа анализатора зависимостей."""

from config import parse_config
from graph_builder import build_npm_graph
from mermaid import graph_to_mermaid
from npm_client import NpmClientError
from test_repository import (
    TestRepositoryError,
    build_test_graph,
    load_test_repository
)


def print_mermaid(graph, versions=None):
    """Вывести описание графа в формате Mermaid."""

    mermaid = graph_to_mermaid(
        graph,
        versions
    )

    print()
    print("Описание графа Mermaid:")
    print()
    print(mermaid)


def run_test_mode(config):
    """Построить граф тестового репозитория."""

    repository = load_test_repository(
        config.repository
    )

    graph = build_test_graph(
        repository,
        config.package,
        config.max_depth
    )

    print_mermaid(graph)


def run_npm_mode(config):
    """Построить граф реального npm-пакета."""

    graph, versions = build_npm_graph(
        config.repository,
        config.package,
        config.version,
        config.max_depth
    )

    print_mermaid(
        graph,
        versions
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