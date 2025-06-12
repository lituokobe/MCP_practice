import json
import os

from openai import OpenAI
from zhipuai import ZhipuAI

#We will use GLM search API here.
#As of June 2025, GLM search standard 0.01CNY/time, pro 0.03CNY/time
#This search is efficient for Chinese queries. Try not to do English search
api_key = os.getenv('GLM_API_KEY')
zhipu_client = ZhipuAI(api_key=api_key,)

def get_weather(location: str):
    print(f"Getting {location} weather...")
    try:
        response = zhipu_client.web_search.web_search(
            search_engine="search-std",
            search_query="以下城市今天的天气 " + location,
            # count=15,  # The number of results to return, ranging from 1-50, default 10
            # search_domain_filter="www.sohu.com",  # Only access content from specified domain names.
            # search_recency_filter="noLimit",  # Search for content within specified date ranges
            # content_size="high"  # Control the word count of webpage summaries, default medium
        )

        print(response)

        if response.search_result:
            return "\n\n". join([d.content for d in response.search_result])

    except Exception as e:
        print(e)
        return "没有搜索到任何内容。"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取某一地点的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如北京、上海、巴塞罗那",
                    }
                },
                "required": ["location"],
            }
        }
    }
]

client = OpenAI()

user_input = "今天南昌的天气怎么样"

resp = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': user_input}],
    tools = tools,
    tool_choice = 'auto', # 'auto' will let the LLM decide whether to call the function. The other 2 values: 'none', 'required'
)

tool_calls = resp.choices[0].message.tool_calls #the tool call
print(tool_calls)
if tool_calls:
    function_name = tool_calls[0].function.name
    function_args = json.loads(tool_calls[0].function.arguments)
    location = function_args['location']

    if function_name == 'get_weather':
        result = get_weather(location)

        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": "", "tool_calls": tool_calls},
                {"role": "tool", "content": result, "tool_call_id": tool_calls[0].id}
            ],
        )
final_answer = second_response.choices[0].message.content

print(f"AI answer: {final_answer}")

