import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from pydantic import BaseModel

load_dotenv()

api_key = os.environ.get("ZHIPUAI_API_KEY")
if not api_key:
    raise ValueError("请在 .env 文件中设置 ZHIPUAI_API_KEY")

llm = ChatOpenAI(
    model="glm-5.3-flash",
    api_key=api_key,
    base_url="https://open.bigmodel.cn/api/paas/v4",
    temperature=0.6
)

@tool
def add(a: int, b: int) -> int:
    """两个整数相加。

    Args:
        a: 第一个整数
        b: 第二个整数
    """
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """两个整数相乘。

    Args:
        a: 第一个整数
        b: 第二个整数
    """
    return a * b

agent = create_agent(
    model=llm, 
    tools=[add, multiply],
    system_prompt="你是一个擅长数学计算的助手，需要计算时调用工具，不要心算。"
)

result = agent.invoke({"messages": [{"role": "user", "content": "帮我算一下 123 + 456，再乘以 7"}]}, 
    config={"recursion_limit": 20}
)

print(result["messages"][-1].content_blocks)