"""Построение графа зависимостей рекурсивным DFS."""

from npm_client import (
    get_dependencies,
    get_dependencies_for_range
)


def build_npm_graph(
    repository,
    package,
    version,
    max_depth
):
    """Построить граф зависимостей реального npm-пакета."""

    graph = {}
    versions = {}
    visited_depth = {}
    active = set()

    def dfs(name, requirement, depth, root=False):
        """Рекурсивно обойти одну вершину графа."""

        previous = visited_depth.get(name)

        if previous is not None and previous <= depth:
            return

        visited_depth[name] = depth

        if root:
            resolved = requirement
            dependencies = get_dependencies(
                repository,
                name,
                resolved
            )
        else:
            resolved, dependencies = (
                get_dependencies_for_range(
                    repository,
                    name,
                    requirement
                )
            )

        versions[name] = resolved
        graph.setdefault(name, [])

        if depth >= max_depth:
            return

        active.add(name)

        for child, child_requirement in dependencies.items():
            if child not in graph[name]:
                graph[name].append(child)

            graph.setdefault(child, [])

            if child not in active:
                dfs(
                    child,
                    child_requirement,
                    depth + 1
                )

        active.remove(name)

    dfs(
        package,
        version,
        0,
        root=True
    )

    return graph, versions