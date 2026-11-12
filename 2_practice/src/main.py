
from config import parse_config


def main():
    # Получаем уже проверенные настройки.
    config = parse_config()

    # На первом этапе просто показываем их пользователю.
    print("=== Анализатор зависимостей npm ===")
    print(f"package: {config.package}")
    print(f"repository: {config.repository}")
    print(f"test_mode: {config.test_mode}")
    print(f"version: {config.version}")
    print(f"max_depth: {config.max_depth}")


# Выполняем main только при прямом запуске файла.
if __name__ == "__main__":
    main()
