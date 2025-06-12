import json
from openai import OpenAI


def get_weather(location: str):
    print(f"Getting {location} weather...")
    weather_data = {
        "location": location,
        "temperature" : "22",
        "condition": "sunny",
        "wind": "level 3",
    }

    return json.dumps(weather_data)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "get weather information of the specified location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City names like Beijing, Barcelona, Buenos Aires",
                    }
                },
                "required": ["location"],
            }
        }
    }
]

client = OpenAI()

user_input = "What's the weather like today in Manipur?"

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

