"""Получение информации о пакетах из npm Registry."""

import json

from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from semver import choose_version


class NpmClientError(Exception):
    """Ошибка получения данных из npm Registry."""


def build_package_url(repository, package, version=None):
    """Создать URL npm Registry."""

    repository = repository.rstrip("/")
    encoded_package = quote(package, safe="")

    if version is None:
        return f"{repository}/{encoded_package}"

    return (
        f"{repository}/{encoded_package}/{version}"
    )


def load_json(url):
    """Получить JSON по указанному URL."""

    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "dependency-visualizer"
        }
    )

    try:
        with urlopen(request, timeout=10) as response:
            data = response.read().decode("utf-8")
    except HTTPError as error:
        raise NpmClientError(
            f"HTTP-ошибка: {error.code}"
        ) from error
    except URLError as error:
        raise NpmClientError(
            f"Ошибка подключения: {error.reason}"
        ) from error

    try:
        return json.loads(data)
    except json.JSONDecodeError as error:
        raise NpmClientError(
            "Получен некорректный JSON"
        ) from error


def fetch_package_metadata(repository, package, version):
    """Получить данные конкретной версии пакета."""

    url = build_package_url(
        repository,
        package,
        version
    )

    return load_json(url)


def fetch_package_document(repository, package):
    """Получить документ со всеми версиями пакета."""

    url = build_package_url(
        repository,
        package
    )

    return load_json(url)


def resolve_version(repository, package, requirement):
    """Преобразовать диапазон npm в конкретную версию."""

    document = fetch_package_document(
        repository,
        package
    )

    versions = document.get(
        "versions",
        {}
    )

    if requirement in versions:
        return requirement

    selected = choose_version(
        versions.keys(),
        requirement
    )

    if selected is None:
        raise NpmClientError(
            f"Не найдена версия {package} для {requirement}"
        )

    return selected


def get_dependencies(repository, package, version):
    """Получить прямые зависимости конкретной версии."""

    metadata = fetch_package_metadata(
        repository,
        package,
        version
    )

    dependencies = metadata.get(
        "dependencies",
        {}
    )

    if not isinstance(dependencies, dict):
        return {}

    return dependencies


def get_dependencies_for_range(
    repository,
    package,
    requirement
):
    """Получить версию и зависимости по npm-диапазону."""

    version = resolve_version(
        repository,
        package,
        requirement
    )

    dependencies = get_dependencies(
        repository,
        package,
        version
    )

    return version, dependencies