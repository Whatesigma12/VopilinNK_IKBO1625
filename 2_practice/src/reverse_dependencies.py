"""Поиск обратных зависимостей пакета."""

from test_repository import build_test_graph


def find_reverse_dependencies(
    repository,
    target,
    max_depth
):
    """
    Найти пакеты, которые зависят от target.

    Для каждого пакета репозитория строится граф
    с помощью DFS из предыдущего этапа.
    """

    reverse = []

    for package in repository:
        # Сам пакет не считаем своей обратной зависимостью.
        if package == target:
            continue

        graph = build_test_graph(
            repository,
            package,
            max_depth
        )

        # Если target встретился в графе этого пакета,
        # значит package зависит от target.
        if target in graph:
            reverse.append(package)

    return sorted(reverse)