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

def get_weather(city: str) -> str:
    """获取指定城市的天气。"""
    return f"{city} 总是阳光明媚！"


class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent(
    model=llm, 
    tools=[get_weather], 
    system_prompt="你是一名乐于助人的助手。回答应简洁、准确。"
)

result = agent.invoke({"messages": [{"role": "user", "content": "雄安新区启动区的天气怎么样？"}]})

print(result["messages"][-1].content_blocks)