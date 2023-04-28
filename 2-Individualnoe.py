#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from pathlib import Path


def tree(dir_path, level, only_dir=-1):
    dir_path = Path(dir_path)
    level += 1
    print(f'+ {dir_path}')
    for path in sorted(dir_path.rglob('*')):
        depth = len(path.relative_to(dir_path).parts)
        if depth < level:
            spacer = '   ' * depth
            if only_dir:
                print(f'{spacer}+ {path.name}')
            else:
                t = Path(path.name)
                if t.is_dir():
                    print(f'{spacer}+ {path.name}')


def main(command_line=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("where", type=str, help="Где искать файлы")

    parser.add_argument("lvl", type=int, help="Уровень поиска")

    parser.add_argument("--show", action='store_false', help="Путь")

    parser.add_argument("--way", type=str, help="Путь")

    args = parser.parse_args(command_line)

    match args.where:
        case "home":
            if args.show:
                tree(Path.home() / args.way, args.lvl, 1)
            else:
                tree(Path.home() / args.way, args.lvl, 0)

        case "cwd":
            if args.show:
                tree(Path.cwd(), args.lvl, 1)
            else:
                tree(Path.cwd(), args.lvl, 0)

        case "mine":
            if args.show:
                tree(args.way, args.lvl, 1)
            else:
                tree(args.way, args.lvl, 0)

        case args.where:
            print(f"Нет варианта - '{args.where}'", file=sys.stderr)
            exit()


if __name__ == "__main__":
    main()
