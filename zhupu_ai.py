import os

from langchain_openai import ChatOpenAI
from zhipuai import ZhipuAI

api_key = os.getenv('GLM_API_KEY')

zhipuai_client = ZhipuAI(api_key=api_key)

llm = ChatOpenAI(
    temperature=0,
    model='glm-4-air-250414',
    api_key=api_key,
    base_url='https://open.bigmodel.cn/api/paas/v4/'
)