"""Минимальные функции работы с версиями npm."""

SEMVER_PARTS = 3
ZERO = 0


def parse_version(version):
    """Преобразовать строку версии в кортеж из трёх чисел."""
    clean = version.split("-", 1)[0]
    parts = clean.split(".")

    if len(parts) != SEMVER_PARTS:
        return None

    try:
        return tuple(int(part) for part in parts)
    except ValueError:
        return None


def satisfies_caret(version, required):
    """Проверить диапазон вида ^1.2.3."""
    current = parse_version(version)
    minimum = parse_version(required)

    if current is None or minimum is None:
        return False

    if minimum[0] > ZERO:
        maximum = (minimum[0] + 1, 0, 0)
    elif minimum[1] > ZERO:
        maximum = (0, minimum[1] + 1, 0)
    else:
        maximum = (0, 0, minimum[2] + 1)

    return minimum <= current < maximum


def satisfies_tilde(version, required):
    """Проверить диапазон вида ~1.2.3."""
    current = parse_version(version)
    minimum = parse_version(required)

    if current is None or minimum is None:
        return False

    maximum = (
        minimum[0],
        minimum[1] + 1,
        0,
    )
    return minimum <= current < maximum


def satisfies(version, requirement):
    """Проверить соответствие версии простому npm-диапазону."""
    requirement = requirement.strip()

    if requirement.startswith("^"):
        return satisfies_caret(version, requirement[1:])
    if requirement.startswith("~"):
        return satisfies_tilde(version, requirement[1:])
    return version == requirement


def choose_version(versions, requirement):
    """Выбрать максимальную подходящую стабильную версию."""
    matching = []

    for version in versions:
        parsed = parse_version(version)
        if parsed is None:
            continue
        if satisfies(version, requirement):
            matching.append((parsed, version))

    if not matching:
        return None

    matching.sort()
    return matching[-1][1]
