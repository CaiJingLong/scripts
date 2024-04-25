#!/usr/bin/env python3

# 这段程序的功能如下:
# 在后台运行一些进程，且报错的时候会自动重启进程而不是退出
# 适合一些 monorepos 有多个项目需要运行 build_runner + asset gen + route gen 的情况，仅需要一次启动
"""
1. 读取 packages 目录下的所有项目中名称包含 -app 的项目
2. 配置需要运行的命令，本程序是 fgen 和 flutter pub run build_runner watch --delete-conflicting-outputs
3. 为每个项目的每个命令创建一个子进程来运行
4. 通过输入小写 q 并回车来“优雅的”退出所有进程，或者你不需要优雅，也可以 ctrl+c 或关闭终端
"""

import multiprocessing
import os
import subprocess
import time
from typing import List

work_dir = os.path.dirname(os.path.abspath(__file__))


class Cmd:
    def __init__(self, cmd: str, cwd: str):
        self.cmd = cmd
        self.cwd = cwd

    def __call__(self):
        while True:
            print(f"running '{self.cmd}' in '{self.cwd}'")
            return_code = subprocess.call(self.cmd, shell=True, cwd=self.cwd)
            print(
                f"'{self.cmd}' in '{self.cwd}' exited with code {return_code}, retrying in 2 seconds"
            )
            time.sleep(2)


project_dirs: List[str] = []

# 找到 packages 目录下的所有项目中名称包含 -app 的项目
# 也可以注释掉这一段，写死在 project_dirs 中
for sub_path in os.listdir("packages"):
    if os.path.isdir(os.path.join("packages", sub_path)):
        if "-app" in sub_path:
            project_dirs.append(os.path.join("packages", sub_path))

# 配置需要运行的命令
cmds = [
    "fgen",
    "flutter pub run build_runner watch --delete-conflicting-outputs",
]


cmd_list: List[Cmd] = []

for project_dir in project_dirs:
    for cmd in cmds:
        cmd_list.append(Cmd(cmd, os.path.join(work_dir, project_dir)))


def watch(cmd: Cmd):
    while True:
        process = subprocess.call(cmd.cmd, shell=True, cwd=cmd.cwd)
        print(f"process {cmd} exited with code {process}")
        print("running watch in 2 seconds")
        time.sleep(2)


if __name__ == "__main__":
    multiprocessing.freeze_support()

    p_list: List[multiprocessing.Process] = []

    for cmd in cmd_list:
        p = multiprocessing.Process(target=cmd)
        p.start()

        p_list.append(p)

    while True:
        input_str = input("q to quit: ")
        print("input_str: ", input_str)
        if input_str == "q":
            print('The input is "q", exiting...')
            for p in p_list:
                p.terminate()
            break
