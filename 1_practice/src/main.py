import argparse
import os
import tkinter as tk
from tkinter import scrolledtext
from commands import (
    exec_cd,
    exec_chmod,
    exec_date,
    exec_head,
    exec_ls,
    exec_touch,
)
from vfs import VFS

MIN_ARGS = 0


def parse_args():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    parser.add_argument("--vfs", default="./vfs_data/minimal", help="Путь VFS")
    parser.add_argument("--script", default=None, help="Стартовый скрипт")
    return parser.parse_args()


class ShellGUI:
    """Графический интерфейс эмулятора оболочки."""

    def __init__(self, root, args):
        """Инициализация окна, VFS и скрипта."""
        self.root = root
        self.args = args
        self.vfs = VFS()
        self.create_widgets()
        self.print_debug_info()
        self.init_vfs()
        if self.args.script:
            self.run_script(self.args.script)

    def init_vfs(self):
        """Загрузка VFS и установка заголовка окна."""
        try:
            self.vfs.load_from_dir(self.args.vfs)
            self.root.title(f"Эмулятор - {self.vfs.name}")
            self.write_output(f"VFS '{self.vfs.name}' успешно загружена.\n")
        except (FileNotFoundError, ValueError) as err:
            self.root.title("Эмулятор - Ошибка VFS")
            self.write_output(f"Ошибка загрузки VFS: {err}\n")

    def create_widgets(self):
        """Создание виджетов окна."""
        self.output = scrolledtext.ScrolledText(
            self.root, width=70, height=20, state="disabled"
        )
        self.output.pack(padx=10, pady=10)
        self.entry = tk.Entry(self.root, width=70)
        self.entry.pack(padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

    def print_debug_info(self):
        """Отладочный вывод параметров."""
        self.write_output("--- Отладочный вывод параметров ---\n")
        self.write_output(f"Путь VFS: {self.args.vfs}\n")
        self.write_output(f"Стартовый скрипт: {self.args.script}\n")
        self.write_output("-----------------------------------\n")

    def write_output(self, text):
        """Вывод текста в терминал."""
        self.output.configure(state="normal")
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.configure(state="disabled")

    def run_script(self, path):
        """Выполнение стартового скрипта."""
        if not os.path.isfile(path):
            self.write_output(f"Ошибка: скрипт '{path}' не найден\n")
            return
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                clean = line.strip()
                if clean:
                    self.process_line(clean)

    def on_enter(self, event=None):
        """Обработка нажатия Enter."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.process_line(line)

    def process_line(self, line):
        """Разбор и выполнение команды."""
        self.write_output(f"{self.vfs.cwd}$ {line}\n")
        parts = line.strip().split()
        if len(parts) == MIN_ARGS:
            return
        self.dispatch(parts[0], parts[1:])

    def dispatch(self, cmd, args):
        """Маршрутизация команд."""
        handlers = {
            "ls": lambda a: exec_ls(self.vfs, a),
            "cd": lambda a: exec_cd(self.vfs, a),
            "date": exec_date,
            "head": lambda a: exec_head(self.vfs, a),
            "touch": lambda a: exec_touch(self.vfs, a),
            "chmod": lambda a: exec_chmod(self.vfs, a),
        }
        if cmd == "exit":
            self.cmd_exit(args)
        elif cmd in handlers:
            self.write_output(handlers[cmd](args))
        else:
            self.write_output(f"Ошибка: неизвестная команда '{cmd}'\n")

    def cmd_exit(self, args):
        """Выход из эмулятора."""
        if len(args) > MIN_ARGS:
            self.write_output("Ошибка: неверные аргументы для exit\n")
            return
        self.root.destroy()


def main():
    """Точка входа."""
    args = parse_args()
    root = tk.Tk()
    ShellGUI(root, args)
    root.mainloop()


if __name__ == "__main__":
    main()