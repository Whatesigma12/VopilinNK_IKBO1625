"""Генерация автономных SVG-схем графа зависимостей."""

from collections import defaultdict, deque
from html import escape

CANVAS_WIDTH = 960
TOP_MARGIN = 90
BOTTOM_MARGIN = 80
SIDE_MARGIN = 90
LEVEL_GAP = 150
NODE_WIDTH = 150
NODE_HEIGHT = 56
NODE_RADIUS = 14
FONT_SIZE = 18
EDGE_WIDTH = 2
BACK_EDGE_OFFSET = 70


def collect_nodes(graph):
    """Вернуть отсортированный список всех вершин графа."""
    nodes = set(graph)
    for dependencies in graph.values():
        nodes.update(dependencies)
    return sorted(nodes)


def _indegrees(graph, nodes):
    """Вычислить количество входящих рёбер для каждой вершины."""
    values = {node: 0 for node in nodes}
    for dependencies in graph.values():
        for dependency in dependencies:
            values[dependency] += 1
    return values


def _fill_levels(graph, levels, start):
    """Заполнить уровни BFS от одной стартовой вершины."""
    queue = deque([start])
    while queue:
        node = queue.popleft()
        next_level = levels[node] + 1
        for child in graph.get(node, []):
            if child in levels:
                continue
            levels[child] = next_level
            queue.append(child)


def _assign_levels(graph, nodes):
    """Назначить вершинам уровни для вертикального расположения."""
    indegrees = _indegrees(graph, nodes)
    roots = [node for node in nodes if indegrees[node] == 0]
    levels = {}

    for root in roots:
        if root not in levels:
            levels[root] = 0
            _fill_levels(graph, levels, root)

    for node in nodes:
        if node not in levels:
            levels[node] = 0
            _fill_levels(graph, levels, node)

    return levels


def _group_levels(levels):
    """Сгруппировать вершины по уровню."""
    groups = defaultdict(list)
    for node, level in levels.items():
        groups[level].append(node)
    for nodes in groups.values():
        nodes.sort()
    return groups


def _positions(levels):
    """Вычислить координаты центров всех вершин."""
    groups = _group_levels(levels)
    positions = {}
    usable_width = CANVAS_WIDTH - 2 * SIDE_MARGIN

    for level, nodes in groups.items():
        step = usable_width / (len(nodes) + 1)
        y_value = TOP_MARGIN + level * LEVEL_GAP
        for index, node in enumerate(nodes, start=1):
            x_value = SIDE_MARGIN + step * index
            positions[node] = (x_value, y_value)

    return positions


def _canvas_height(levels):
    """Вычислить высоту SVG по количеству уровней."""
    highest = max(levels.values(), default=0)
    content = TOP_MARGIN + highest * LEVEL_GAP
    return int(content + NODE_HEIGHT + BOTTOM_MARGIN)


def _forward_path(source, target):
    """Сформировать плавное ребро к вершине на нижнем уровне."""
    source_x, source_y = source
    target_x, target_y = target
    start_y = source_y + NODE_HEIGHT / 2
    end_y = target_y - NODE_HEIGHT / 2
    middle_y = (start_y + end_y) / 2
    return (
        f"M {source_x:.1f} {start_y:.1f} "
        f"C {source_x:.1f} {middle_y:.1f}, "
        f"{target_x:.1f} {middle_y:.1f}, "
        f"{target_x:.1f} {end_y:.1f}"
    )


def _back_path(source, target):
    """Сформировать дугу для обратного ребра или цикла."""
    source_x, source_y = source
    target_x, target_y = target
    start_x = source_x - NODE_WIDTH / 2
    end_x = target_x - NODE_WIDTH / 2
    bend_x = min(start_x, end_x) - BACK_EDGE_OFFSET
    return (
        f"M {start_x:.1f} {source_y:.1f} "
        f"C {bend_x:.1f} {source_y:.1f}, "
        f"{bend_x:.1f} {target_y:.1f}, "
        f"{end_x:.1f} {target_y:.1f}"
    )


def _edge_path(source, target):
    """Выбрать форму ребра по направлению между уровнями."""
    if target[1] > source[1]:
        return _forward_path(source, target)
    return _back_path(source, target)


def _edge_lines(graph, positions):
    """Сформировать SVG-пути всех рёбер."""
    lines = []
    for node in sorted(graph):
        for dependency in sorted(graph[node]):
            path = _edge_path(
                positions[node],
                positions[dependency],
            )
            edge_name = escape(
                f"{node}->{dependency}",
                quote=True,
            )
            lines.append(
                "    <path class=\"edge\" "
                f"data-edge=\"{edge_name}\" d=\"{path}\" />"
            )
    return lines


def _node_lines(nodes, positions):
    """Сформировать SVG-элементы всех вершин."""
    lines = []
    half_width = NODE_WIDTH / 2
    half_height = NODE_HEIGHT / 2

    for node in nodes:
        x_value, y_value = positions[node]
        left = x_value - half_width
        top = y_value - half_height
        label = escape(node)
        attribute = escape(node, quote=True)
        lines.extend([
            f'    <g class="node" data-node="{attribute}">',
            (
                f'      <rect x="{left:.1f}" y="{top:.1f}" '
                f'width="{NODE_WIDTH}" height="{NODE_HEIGHT}" '
                f'rx="{NODE_RADIUS}" />'
            ),
            (
                f'      <text x="{x_value:.1f}" y="{y_value:.1f}">'
                f'{label}</text>'
            ),
            "    </g>",
        ])

    return lines


def _header(height, title):
    """Сформировать начало автономного SVG-документа."""
    safe_title = escape(title)
    return [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{CANVAS_WIDTH}" height="{height}" '
            f'viewBox="0 0 {CANVAS_WIDTH} {height}">'
        ),
        "  <defs>",
        (
            '    <linearGradient id="nodeGradient" '
            'x1="0" y1="0" x2="0" y2="1">'
        ),
        '      <stop offset="0%" stop-color="#ffffff" />',
        '      <stop offset="100%" stop-color="#e8f0ff" />',
        "    </linearGradient>",
        (
            '    <marker id="arrow" markerWidth="10" '
            'markerHeight="8" refX="9" refY="4" orient="auto">'
        ),
        '      <path d="M 0 0 L 10 4 L 0 8 z" fill="#365f9d" />',
        "    </marker>",
        "  </defs>",
        "  <style>",
        '    .background { fill: #f7f9fc; }',
        (
            '    .edge { fill: none; stroke: #365f9d; '
            f'stroke-width: {EDGE_WIDTH}; marker-end: url(#arrow); }}'
        ),
        (
            '    .node rect { fill: url(#nodeGradient); '
            'stroke: #2f5597; stroke-width: 2; }'
        ),
        (
            '    .node text { fill: #17365d; font-family: '
            f'Arial, sans-serif; font-size: {FONT_SIZE}px; '
            'font-weight: 700; text-anchor: middle; '
            'dominant-baseline: middle; }'
        ),
        (
            '    .title { fill: #17365d; font-family: '
            'Arial, sans-serif; font-size: 24px; '
            'font-weight: 700; text-anchor: middle; }'
        ),
        "  </style>",
        (
            f'  <rect class="background" x="0" y="0" '
            f'width="{CANVAS_WIDTH}" height="{height}" />'
        ),
        (
            f'  <text class="title" x="{CANVAS_WIDTH / 2:.1f}" '
            f'y="38">{safe_title}</text>'
        ),
        '  <g class="edges">',
    ]


def graph_to_svg(graph, title="Dependency graph"):
    """Преобразовать граф зависимостей в автономное SVG-изображение."""
    nodes = collect_nodes(graph)
    levels = _assign_levels(graph, nodes)
    positions = _positions(levels)
    height = _canvas_height(levels)

    lines = _header(height, title)
    lines.extend(_edge_lines(graph, positions))
    lines.append("  </g>")
    lines.append('  <g class="nodes">')
    lines.extend(_node_lines(nodes, positions))
    lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines)
