#!/opt/homebrew/Caskroom/miniconda/base/bin/python

import glob
import tiktoken
import argparse
import os

def calculate_file_tokens(file_path, encoding):
    """
    计算单个文件的上下文 token 数量。

    :param file_path: 要分析的文件路径
    :param encoding: tiktoken 的编码器对象
    :return: 文件的 token 数
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tokens = encoding.encode(content)
        token_count = len(tokens)
        # 使用相对路径显示文件
        relative_path = os.path.relpath(file_path)
        print(f"文件 {relative_path} 包含的 token 数量: {token_count}")
        return token_count
    except FileNotFoundError:
        relative_path = os.path.relpath(file_path)
        print(f"错误：文件 {relative_path} 不存在！")
        return 0
    except Exception as e:
        relative_path = os.path.relpath(file_path)
        print(f"分析文件 {relative_path} 时出错：{e}")
        return 0

def calculate_tokens_for_glob(pattern, encoding_name):
    """
    根据 glob 模式匹配文件，并计算所有文件的 token 总数。

    :param pattern: 文件匹配模式 (如 "*.txt" 或 "data/*.md")，可以是单个模式或模式列表
    :param encoding_name: 使用的模型对应的编码名称
    :return: 总 token 数
    """
    encoding = tiktoken.encoding_for_model(encoding_name)
    total_tokens = 0
    total_files = 0

    # 确保pattern是列表形式
    patterns = pattern if isinstance(pattern, list) else [pattern]
    
    for current_pattern in patterns:
        # 使用 glob 匹配文件
        file_paths = glob.glob(current_pattern, recursive=True)
        if not file_paths:
            print(f"未找到匹配的文件，模式为: {current_pattern}")
            continue

        pattern_file_count = len(file_paths)
        total_files += pattern_file_count
        print(f"匹配到 {pattern_file_count} 个文件，模式为: {current_pattern}")
        
        for file_path in file_paths:
            total_tokens += calculate_file_tokens(file_path, encoding)
    
    if total_files > 0:
        print(f"\n总计匹配到 {total_files} 个文件，总 token 数量: {total_tokens}")
    else:
        print("未找到任何匹配的文件")
    
    return total_tokens

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="计算匹配文件的总 token 数量")
    parser.add_argument("patterns", type=str, nargs='+', help="文件匹配模式，可以指定多个 (如 '*.txt' 'data/**/*.md')")
    parser.add_argument(
        "--model", 
        type=str, 
        default="gpt-4o", 
        help="使用的模型名称 (默认为 gpt-4o)"
    )

    args = parser.parse_args()

    # 调用计算函数
    calculate_tokens_for_glob(args.patterns, args.model)
