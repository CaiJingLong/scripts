#!/usr/bin/env python
# 指定一个目录，提取其中的所有代码文件，将其内容提取到同文件中
# 使用方法：python extract_code.py -s <src_dir> -d <dst_file> -exts <exts>
import argparse
import os


def extract_code(src_dir, dst_file, exts: str):
    abs_dst_file = os.path.abspath(dst_file)
    abs_src_dir = os.path.abspath(src_dir)

    if not os.path.exists(src_dir):
        print("Source directory {} not exists".format(abs_src_dir))
        return

    if not os.path.isdir(src_dir):
        print("Source directory {} is not a directory".format(abs_src_dir))
        return

    if not os.path.exists(dst_file):
        print("Destination file {} not exists, will create".format(abs_dst_file))
        os.makedirs(os.path.dirname(abs_dst_file), exist_ok=True)

    exts = exts.split(",")
    with open(dst_file, "w") as dst_fp:
        text = ""
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                for ext in exts:
                    if file.endswith(ext):
                        with open(os.path.join(root, file), "r") as src_fp:
                            # dst_fp.write(src_fp.read())
                            # dst_fp.write("\n")
                            text += src_fp.read()

        # 去除空行
        lines = text.split("\n")
        text = "\n".join([line for line in lines if line.strip() != ""])

        dst_fp.write(text)

    print("Extracted code from {} to {}".format(abs_src_dir, abs_dst_file))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=str, help="source directory")
    parser.add_argument("-d", type=str, help="destination file", default="code.txt")
    parser.add_argument("-exts", type=str, help="file extensions", default=".dart")
    args = parser.parse_args()
    extract_code(args.s, args.d, args.exts)


if __name__ == "__main__":
    main()
