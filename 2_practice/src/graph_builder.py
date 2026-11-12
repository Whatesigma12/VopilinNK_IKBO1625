"""Построение графа зависимостей рекурсивным DFS."""

from npm_client import (
    get_dependencies,
    get_dependencies_for_range,
)


class NpmGraphBuilder:
    """Строитель графа зависимостей npm."""

    def __init__(self, repository, max_depth):
        """Сохранить параметры и подготовить состояние обхода."""
        self.repository = repository
        self.max_depth = max_depth
        self.graph = {}
        self.versions = {}
        self.visited_depth = {}
        self.active = set()

    def build(self, package, version):
        """Построить граф от указанного пакета."""
        self._dfs(package, version, 0, root=True)
        return self.graph, self.versions

    def _load_dependencies(self, name, requirement, root):
        """Получить конкретную версию и зависимости вершины."""
        if root:
            dependencies = get_dependencies(
                self.repository,
                name,
                requirement,
            )
            return requirement, dependencies

        return get_dependencies_for_range(
            self.repository,
            name,
            requirement,
        )

    def _should_skip(self, name, depth):
        """Проверить, был ли пакет посещён на меньшей глубине."""
        previous = self.visited_depth.get(name)
        return previous is not None and previous <= depth

    def _add_edges(self, name, dependencies):
        """Добавить исходящие рёбра вершины."""
        for child in dependencies:
            if child not in self.graph[name]:
                self.graph[name].append(child)
            self.graph.setdefault(child, [])

    def _dfs(self, name, requirement, depth, root=False):
        """Рекурсивно обойти одну вершину графа."""
        if self._should_skip(name, depth):
            return

        self.visited_depth[name] = depth
        resolved, dependencies = self._load_dependencies(
            name,
            requirement,
            root,
        )
        self.versions[name] = resolved
        self.graph.setdefault(name, [])

        if depth >= self.max_depth:
            return

        self.active.add(name)
        self._add_edges(name, dependencies)
        self._visit_children(dependencies, depth)
        self.active.remove(name)

    def _visit_children(self, dependencies, depth):
        """Рекурсивно посетить дочерние зависимости."""
        for child, requirement in dependencies.items():
            if child in self.active:
                continue
            self._dfs(
                child,
                requirement,
                depth + 1,
            )


def build_npm_graph(repository, package, version, max_depth):
    """Построить граф зависимостей реального npm-пакета."""
    builder = NpmGraphBuilder(repository, max_depth)
    return builder.build(package, version)
