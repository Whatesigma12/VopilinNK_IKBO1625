"""Тесты выбора npm-версий."""

import sys
import unittest

from pathlib import Path


sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1]
        / "src"
    )
)


from semver import (
    choose_version,
    satisfies
)


class TestSemver(unittest.TestCase):
    """Проверка диапазонов версий."""

    def test_exact_version(self):
        """Точная версия должна совпадать."""

        self.assertTrue(
            satisfies(
                "1.2.3",
                "1.2.3"
            )
        )

    def test_caret_version(self):
        """Caret должен разрешать версию того же major."""

        self.assertTrue(
            satisfies(
                "1.9.0",
                "^1.2.3"
            )
        )

        self.assertFalse(
            satisfies(
                "2.0.0",
                "^1.2.3"
            )
        )

    def test_tilde_version(self):
        """Tilde должен разрешать версию того же minor."""

        self.assertTrue(
            satisfies(
                "1.3.9",
                "~1.3.8"
            )
        )

        self.assertFalse(
            satisfies(
                "1.4.0",
                "~1.3.8"
            )
        )

    def test_choose_latest_matching(self):
        """Выбирается максимальная подходящая версия."""

        versions = [
            "1.3.8",
            "1.3.9",
            "1.4.0"
        ]

        result = choose_version(
            versions,
            "~1.3.8"
        )

        self.assertEqual(
            result,
            "1.3.9"
        )


if __name__ == "__main__":
    unittest.main()