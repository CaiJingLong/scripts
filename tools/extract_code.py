# 用于生成一个文件，应该是用于软著
# 打开源码目录，提取出指定 extension 的文件，拼接到一起，生成一个文件
# 使用方式，放在 "源码/scripts" 下 ，执行 python extract_code.py 即可

import os
import sys


def get_files(path: str, extenstions: list[str], exclude_names: list[str] = []):
    """获取指定目录下所有指定后缀的文件"""

    print("path:", path)
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename in exclude_names:
                continue
            for ext in extenstions:
                if filename.endswith(ext):
                    files.append(os.path.join(root, filename))
    return files


cwd = sys.path[0]

files = get_files(f"{cwd}/..", [".java", ".kt"])
dart_files = get_files(
    f"{cwd}/..",
    [".dart"],
    [
        "url.dart",
        "http_utils.dart",
        "main.dart",
        "app.dart",
    ],
)

files.extend(dart_files)

print(f"共找到 {len(files)} 个文件")
print(f"文件列表：{files}")

result = f"{cwd}/../logs/result.txt"

if os.path.exists(result):
    os.remove(result)

if os.path.exists(f"{cwd}/../logs"):
    os.rmdir(f"{cwd}/../logs")

ignore_contents = [
    "Generated file",
    "void main()",
    "Generate by",
    "Automatically generated file",
    "Copyright (C) 2016 The Android Open Source Project",
]

for file in files:
    with open(file, "r") as f:
        content = f.read()

        if any([ignore_content in content for ignore_content in ignore_contents]):
            continue

        lines = content.split("\n")
        content = "\n".join([line for line in lines if line.strip() != ""])
        with open(result, "a+") as r:
            r.write(f"{content}\n")

print(f"提取完成，结果保存在 {result}")
