#!/usr/bin/env python

## 显示安卓项目的依赖，这里强制写死了 module 名为 app，可以自行修改
## 用法： show_android_deps.py <android-path>

import os
import re
import sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <path to android>")
    sys.exit(1)

android_path = sys.argv[1]

cmd = "./gradlew app:dependencies"

os.chdir(android_path)

output = os.popen(cmd).read()

# print("lines: ", output)

lines = output.split("\n")

regex = r"(\S+):(\S+):(\S+)"


class Dep:
    def __init__(self, group, name, version):
        self.group = group
        self.name = name
        self.version = version

    def parse(text: str):
        # org.jetbrains.kotlin:kotlin-compiler-embeddable:1.8.10
        match = re.match(regex, text)
        if match:
            return Dep(match.group(1), match.group(2), match.group(3))
        else:
            return None


dep_list: list[Dep] = []

for line in lines:
    found_text = re.findall(regex, line)
    if len(found_text) > 0:
        for text in found_text:
            if text[0] == "https" or text[0] == "http":
                continue
            dep = Dep(text[0], text[1], text[2])
            dep_list.append(dep)


dep_dict = {}

for dep in dep_list:
    key = f"{dep.group}:{dep.name}"

    if key in dep_dict:
        dep_dict[key] += 1
    else:
        dep_dict[key] = 1

for key in dep_dict:
    print("key: ", key)

print(f"Total dependencies: {len(dep_dict)}")
