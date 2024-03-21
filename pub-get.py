#!/usr/bin/env python3

# 脚本功能，在当前工作目录下的所有 flutter/dart 目录都执行一次 dart pub get

import os

working_directory = os.getcwd()

# find all pubspec.yaml files
pubspec_files = []

for root, dirs, files in os.walk(working_directory):
    for file in files:
        if file == "pubspec.yaml":
            pubspec_files.append(os.path.join(root, file))


# run pub get for each pubspec.yaml file
            
for pubspec in pubspec_files:
    print("Running pub get for:", pubspec)
    os.system("cd " + os.path.dirname(pubspec) + " && flutter pub get")
