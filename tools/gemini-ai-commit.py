#!/opt/homebrew/Caskroom/miniconda/base/bin/python
'''
这个文件使用 gemini api 的 gemini-2.0-flash-exp 模型来生成 commit message
你可以自行替换 `prompt` 中的内容来调整生成的内容
也可以自行替换 Gemini 的 api，并使用其他的 AI，比如 openai ollama 等

如果你使用 GEMINI 的 api，需要安装如下的库
pip install google-genai python-dotenv

并设置 .env 文件在 此文件的同名目录下，内容为
GEMINI_API_KEY=你的 API key
'''

import warnings

warnings.filterwarnings("ignore", message=".*grpc_wait_for_shutdown_with_timeout.*")

# 0. 记录当前目录
import os
cur_dir = os.getcwd()

# 1. 设置当前 script 所在目录为工作目录
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 2. 读取 .env 文件
from dotenv import load_dotenv
load_dotenv()

# 3. 获取环境变量 GEMINI_API_KEY
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.chdir(cur_dir)

def call_cmd(cmd: str, contains_err: bool = False) -> str:
  import subprocess
  ret = subprocess.run(cmd, shell=True, text=True, capture_output=True)
  if ret.returncode != 0:
    print(ret.stderr)
    if not contains_err:
      exit(1)
  return ret.stdout.strip()

# 4. 读取当前准备提交的目录
cmd = 'git diff --staged'
# 读取输出内容
diff = call_cmd(cmd)
print('读取 git diff 结果成功，现在开始调用 AI 生成 commit message')

# 5. 使用 AI 总结内容， gemini api 调用
prompt = f"""
这个是 AI-Commit 插件的 prompts，用于自动根据 [conventional commit conventio][ccc] 规范来生成内容

[ccc]: https://www.conventionalcommits.org/en/v1.0.0/

你根据 git 提交记录来创建 commit messages，应该遵循 conventional commit conventio 规范.

要遵守如下要求:

- 你应该使用中文而不是英文
- 你创建的内容应该不包含 ``` 代码块
- 其中 <type> 代表了规范中提及的类型，以下是 type 应该包含的列表
  - build
  - chore
  - ci
  - docs
  - feat
  - fix
  - perf
  - refactor
  - revert
  - style
  - test
- <title> 表示本次主要修改了什么信息
- <item?> 表示修改的详情
- 单行不能超过74个字符
- 仅包含一个 type 行
- 文件名使用 ` 字符包裹
- 如果 items 很多，但明显表述的内容为一个很一眼可知的，如配置文件、版本号之类的情况，可以不使用 items，仅使用 type 即可

以下是一个模板:


<type>: <title>

- <item1>
- <item2>

这是一个示例:

chore: 更新了依赖

- 本次升级了 junit 的版本号


如下是 git commit diff: 
{diff}
```
""".strip()

## 引入 google 的 gemini api
def call_gemini_api(prompt):
  print('请稍候，正在请求 AI 生成 commit message\n')

  import google.generativeai as genai

  genai.configure(api_key=GEMINI_API_KEY)
  model = genai.GenerativeModel("gemini-2.0-flash-exp")
  response = model.generate_content(prompt)
  res = response.text.strip()

  return res

while True:
  response = call_gemini_api(prompt)
  
  # 输出生成的 commit message 到 log 中，并询问用户是否满意
  print(response)
  print('\n')
  print('是否满意?')
  print('  y:满意，r:重试，e:退出')
  confirm = input('输入你的选择: ')
  
  if confirm == "y":
    break
  elif confirm == "r":
    continue
  else:
    exit(0)


# 6. 提交

## 6.1 找到当前 git 的根目录
cmd = 'git rev-parse --show-toplevel'
root_dir = call_cmd(cmd)
print('当前 git 根目录:', root_dir)

## 创建一个特殊文件 .git/COMMIT_TMP_FILE
tmp_file = f'{root_dir}/.git/COMMIT_TMP_FILE'
with open(tmp_file, 'w') as f:
  f.write(response)

## 6.2 提交
cmd = f'git commit -F {tmp_file}'
ret = call_cmd(cmd)
print(ret)

## 6.3 删除临时文件
os.remove(tmp_file)

## 提示提交成功
print('提交成功')
