import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class NpmClientError(Exception):
    """Ошибка при получении данных из npm Registry."""


def build_package_url(repository, package, version):
    """
    Создаёт URL для получения информации
    о конкретной версии npm-пакета.
    """

    # Удаляем возможный / в конце адреса репозитория.
    repository = repository.rstrip("/")

    # Кодируем имя пакета для безопасной передачи в URL.
    # Это особенно важно для scoped-пакетов:
    # например @babel/core.
    encoded_package = quote(package, safe="")

    return f"{repository}/{encoded_package}/{version}"


def fetch_package_metadata(repository, package, version):
    """
    Получает JSON с информацией о пакете
    из npm Registry.
    """

    url = build_package_url(
        repository,
        package,
        version
    )

    # Создаём HTTP-запрос.
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "dependency-visualizer"
        }
    )

    try:
        # Отправляем запрос.
        with urlopen(request, timeout=10) as response:

            # Получаем байты и превращаем их в текст.
            data = response.read().decode("utf-8")

    except HTTPError as error:

        if error.code == 404:
            raise NpmClientError(
                f"Пакет '{package}' версии '{version}' не найден"
            )

        raise NpmClientError(
            f"HTTP-ошибка npm Registry: {error.code}"
        )

    except URLError as error:
        raise NpmClientError(
            f"Не удалось подключиться к npm Registry: {error.reason}"
        )

    except TimeoutError:
        raise NpmClientError(
            "Превышено время ожидания ответа npm Registry"
        )

    try:
        # Преобразуем JSON-текст в Python-словарь.
        return json.loads(data)

    except json.JSONDecodeError:
        raise NpmClientError(
            "npm Registry вернул некорректный JSON"
        )


def get_dependencies(repository, package, version):
    """
    Возвращает прямые зависимости указанной версии пакета.

    Результат:
    {
        "accepts": "~1.3.8",
        "array-flatten": "1.1.1",
        ...
    }
    """

    metadata = fetch_package_metadata(
        repository,
        package,
        version
    )

    dependencies = metadata.get(
        "dependencies",
        {}
    )

    # Иногда поле dependencies может отсутствовать.
    # В этом случае просто возвращаем пустой словарь.
    if not isinstance(dependencies, dict):
        return {}

    return dependencies