# fde-agent-mini

基于 LangChain 与智谱 GLM 模型的轻量级 Agent 示例，包含天气查询助手与数学计算助手。

## 功能

- `firstAgent.py`：演示工具调用（天气查询），让 Agent 在回答中使用自定义工具。他是一个简单的天气查询助手，他解决的问题是告知用户某地的天气情况，但是目前他仅能输出固定的天气信息。
- `calcAgent.py`：演示多步工具链（加法 → 乘法），完成复合数学运算。他是一个简单的数据计算助手，他解决的问题是告知用户两个数字的加法和乘法运算结果，目前他仅能执行加法和乘法两种运算。

## 环境依赖

- Python 3.14
- 依赖包：`langchain`、`langchain-openai`、`python-dotenv`、`pydantic`

在虚拟环境中安装依赖：

```powershell
& "c:\Users\10533\WorkBuddy\spaces\2026_11_24_11-11-24\.venv\Scripts\python.exe" -m pip install langchain langchain-openai python-dotenv pydantic
```

## 配置

在项目根目录创建 `.env` 文件，填入智谱 API Key：

```
ZHIPUAI_API_KEY=你的API密钥
```

`.env` 已被 `.gitignore` 忽略，不会提交到 Git 仓库。

## 运行命令

### 方式一：直接用虚拟环境的 Python 运行

```powershell
& "c:\Users\10533\WorkBuddy\spaces\2026_11_24_11-11-24\.venv\Scripts\python.exe" "c:\Users\10533\WorkBuddy\spaces\2026_11_24_11-11-24\fde-agent-mini\firstAgent.py"
```

```powershell
& "c:\Users\10533\WorkBuddy\spaces\2026_11_24_11-11-24\.venv\Scripts\python.exe" "c:\Users\10533\WorkBuddy\spaces\2026_11_24_11-11-24\fde-agent-mini\calcAgent.py"
```

### 方式二：先激活虚拟环境再运行

```powershell
cd c:\Users\10533\WorkBuddy\spaces\2026_11_24_11-11-24
.\.venv\Scripts\Activate.ps1
python fde-agent-mini\firstAgent.py
python fde-agent-mini\calcAgent.py
```

## 真实运行日志

### firstAgent.py

```
[{'type': 'text', 'text': '雄安新区启动区的天气非常晴朗，总是阳光明媚！☀️'}]
```

### calcAgent.py

```
[{'type': 'text', 'text': '计算完成！\n\n**(123 + 456) × 7 = 4053**\n\n计算过程：\n1. 123 + 456 = 579\n2. 579 × 7 = 4053'}]
```
