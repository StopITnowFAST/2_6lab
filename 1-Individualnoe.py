#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import argparse
import os.path
import sys
import json


def add_st(staff, name, group, lmarks):
    """
    Ввести данные студента в словарь
    """
    staff.append({"name": name, "group": group, "marks": lmarks})

    return staff


def show(staff):
    """
    Вывод записей всего словаря
    """
    if staff:
        line = "+-{}-+-{}-+-{}-+-{}-+".format("-" * 4, "-" * 30, "-" * 20, "-" * 15)
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^15} |".format(
                "№", "Ф.И.О.", "Группа", "Успеваемость"
            )
        )
        print(line)

        for idx, student in enumerate(staff, 1):
            lmarks = student.get("marks", "")
            print(
                "| {:>4} | {:<30} | {:<20} | {:>15} |".format(
                    idx,
                    student.get("name", ""),
                    student.get("group", ""),
                    " ".join(map(str, lmarks)),
                )
            )
        print(line)
    else:
        print("Список пуст")


def marks(staff):
    """
    Вывод фамилий и номеров групп, студентов имеющих 2
    """
    count = 0
    line = "+-{}-+-{}-+".format("-" * 30, "-" * 10)
    for student in staff:
        if 2 in student.get("marks"):
            count += 1
            if count == 1:
                print(line)
            print(
                "| {:<30} | {:^10} |".format(
                    student.get("name", ""),
                    student.get("group", ""),
                )
            )
            print(line)

    if count == 0:
        print("Студенты не найдены.")


def save_students(file_name, staff):
    """
    Сохранить всех студентов в файл JSON
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    """
    Загрузить всех работников из файла JSON
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d", "--data", action="store", required=False, help="The data file name"
    )

    parser = argparse.ArgumentParser("students")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add", parents=[file_parser], help="Add a new student")

    add.add_argument(
        "-n", "--name", action="store", required=True, help="The student's name"
    )
    add.add_argument(
        "-g", "--group", action="store", required=True, help="The student's group"
    )
    add.add_argument(
        "-m",
        "--marks",
        action="store",
        type=list,
        required=True,
        help="The student's marks",
    )

    showmarks = subparsers.add_parser(
        "showmarks", parents=[file_parser], help="Show students with mark 2"
    )

    _ = subparsers.add_parser(
        "show", parents=[file_parser], help="Display all students"
    )

    args = parser.parse_args(command_line)

    file = "\stud.json"
    data_file = args.data
    if not data_file:
        data_file = str(pathlib.Path.home()) + file
    if not data_file:
        print("The data file name is missing", file=sys.stderr)
        sys.exit(1)

    is_dirty = False
    if os.path.exists(data_file):
        students = load_students(data_file)
    else:
        students = []

    if args.command == "add":
        buf = [int(a) for a in args.marks]
        rightmarks = list(filter(lambda x: 0 < x < 6, buf))
        if len(rightmarks) != 5:
            print("ошибка в количестве или значении оценок", file=sys.stderr)
            exit()
        students = add_st(students, args.name, args.group, rightmarks)
        is_dirty = True

    elif args.command == "show":
        show(students)

    elif args.command == "showmarks":
        marks(students)

    if is_dirty:
        save_students(data_file, students)


if __name__ == "__main__":
    main()
