from config import parse_config
from npm_client import NpmClientError, get_dependencies


def main():

    # Получаем параметры командной строки.
    config = parse_config()

    print("=== Анализатор зависимостей npm ===")

    print(f"Пакет: {config.package}")
    print(f"Версия: {config.version}")
    print(f"Репозиторий: {config.repository}")
    print(f"Максимальная глубина: {config.max_depth}")

    # На втором этапе обычный режим уже
    # получает реальные зависимости из npm.
    if not config.test_mode:

        try:

            dependencies = get_dependencies(
                config.repository,
                config.package,
                config.version
            )

        except NpmClientError as error:

            print()
            print(f"Ошибка: {error}")

            return 1

        print()
        print("Прямые зависимости:")

        # Если зависимостей нет.
        if not dependencies:

            print("Нет зависимостей")

            return 0

        # Сортируем зависимости по имени,
        # чтобы вывод всегда был одинаковым.
        for name in sorted(dependencies):

            version = dependencies[name]

            print(
                f"- {name}: {version}"
            )

    else:

        print()
        print("Тестовый режим будет реализован на следующих этапах.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())