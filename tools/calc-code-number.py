#!/usr/bin/env python3

import os

import argparse

parser = argparse.ArgumentParser(description="Calculate code number.")

parser.add_argument(
    "-d",
    "--dir",
    type=str,
    default=".",
    help="The directory to calculate code number.",
)

parser.add_argument(
    "-e",
    "--ext",
    type=str,
    default="",
    help="The file extension to calculate code number.",
)

parser.add_argument(
    "-c",
    "--check-empty-line",
    action="store_true",
    help="Check empty line or not.",
)

parser.add_argument(
    "-i",
    "--ignore-path",
    type=str,
    default="",
    help="Ignore path.",
)

args = parser.parse_args()


def get_line_number(file):
    count = 0
    empty = 0
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            count += 1
            if line.strip() == "":
                empty += 1
    return count, empty


if __name__ == "__main__":
    dir_path = args.dir

    if args.ext == "":
        print("Please input file extension. Use -e to define.")
        exit(1)

    ext_list = args.ext.split(",")
    check_empty_line = args.check_empty_line
    ignore_path = args.ignore_path
    for i in range(len(ext_list)):
        ext_list[i] = ext_list[i].strip()

    dirs = os.walk(dir_path)

    total_file_count = 0
    lines = 0
    empty_lines = 0

    for dir in dirs:
        for file in dir[2]:
            if file.endswith(tuple(ext_list)):
                total_file_count += 1
                file_path = f"{dir[0]}/{file}"

                if ignore_path != "" and file_path.find(ignore_path) != -1:
                    continue

                line_count, empty_count = get_line_number(file_path)

                lines += line_count
                empty_lines += empty_count

    print(f"file count: {total_file_count}")
    print(f"line count: {lines}")
    print(f"empty line count: {empty_lines}")
    print(f"non-empty line count: {lines - empty_lines}")
