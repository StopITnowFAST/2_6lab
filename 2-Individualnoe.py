#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from pathlib import Path
from itertools import islice

space = "    "
branch = "│   "
tee = "├── "
last = "└── "


def tree(dir_path, level=-1, limit_to_directories=False, length_limit=1000):
    dir_path = Path(dir_path)
    files = 0
    directories = 0

    def inner(dir_path, prefix="", level=-1):
        nonlocal files, directories

        if not level:
            return

        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]

        else:
            contents = list(dir_path.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]

        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space
                yield from inner(path, prefix=prefix + extension, level=level - 1)

            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1

    print(dir_path.name)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    print(f"\n{directories} Каталогов" + (f", {files} Файлов" if files else ""))


def main(command_line=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("where", type=str, help="Где искать файлы")

    parser.add_argument("lvl", type=int, help="Уровень поиска")

    parser.add_argument("--way", type=str, help="Путь")

    parser.add_argument(
        "-s", "--show", action="store_true", help="Показать только каталог"
    )

    args = parser.parse_args(command_line)

    match args.where:
        case "home":
            if args.show:
                if args.lvl > 0:
                    tree(Path.home() / args.way, args.lvl, True)
                else:
                    tree(Path.home() / args.way, True)
            else:
                if args.lvl > 0:
                    tree(Path.home() / args.way, args.lvl)
                else:
                    tree(Path.home() / args.way)

        case "cwd":
            if args.show:
                if args.lvl > 0:
                    tree(Path.cwd(), args.lvl, True)
                else:
                    tree(Path.cwd(), True)
            else:
                if args.lvl > 0:
                    tree(Path.cwd(), args.lvl)
                else:
                    tree(Path.cwd())

        case "mine":
            if args.show:
                if args.lvl > 0:
                    tree(args.way, args.lvl, True)
                else:
                    tree(args.way, True)
            else:
                if args.lvl > 0:
                    tree(args.way, args.lvl)
                else:
                    tree(args.way)

        case args.where:
            print(f"Нет варианта - '{args.where}'", file=sys.stderr)
            exit()


if __name__ == "__main__":
    main()
