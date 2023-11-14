import os

script_path = os.path.dirname(os.path.abspath(__file__))

ext = '.kt,.java'

ext_list = ext.split(',')

for i in range(len(ext_list)):
    ext_list[i] = ext_list[i].strip()


def get_line_number(file, check_empty_line=False):
    count = 0
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if check_empty_line:
                if line.strip() != '':
                    count += 1
            else:
                count += 1
    return count


if __name__ == '__main__':
    dir_path = f'{script_path}/../src'
    dirs = os.walk(dir_path)

    total_file_count = 0
    lines = 0
    empty_lines = 0

    for dir in dirs:
        for file in dir[2]:
            if file.endswith(tuple(ext_list)):
                total_file_count += 1
                file_path = f'{dir[0]}/{file}'
                line_count = get_line_number(file_path)
                empty_line_count = get_line_number(file_path, True)
                lines += line_count
                empty_lines += empty_line_count
                print(f'{file_path} | {line_count} | {empty_line_count}')

    print(f'file count: {total_file_count}')
    print(f'line count: {lines}')
    print(f'empty line count: {empty_lines}')
