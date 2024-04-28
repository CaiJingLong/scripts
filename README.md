# scripts

放一些和项目具体无关，但偶尔会用到的脚本

## 目录

[watch.py](watch.py) 批量管理运行的命令，比如 build_runner + fgen + 其他需要生成的东西，在失败时会自动重试，比如 flutter pub get 会退出 build_runner，但是这个脚本会自动重启它。

[tools/calc-code-number.py](tools/calc-code-number.py) 用于计算代码行数

[tools/extract_code.py](tools/extract_code.py) 提取文件并合并到一个文件内，一般用于软著等需要这么做的情况
