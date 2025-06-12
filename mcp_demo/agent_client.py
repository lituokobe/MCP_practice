import asyncio

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mcp_adapters.client import MultiServerMCPClient

from MCP_practice.zhupu_ai import llm

#define the configuration dictionary for remote MCP server
mcp_server_config = {
    "url": "http://localhost:8008/sse", #defined in mcp_server.py
    "transport": "sse", #remote server only supports sse by June 2025
}

prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个智能助手，尽可能的调用工具回答用户的问题'),
    MessagesPlaceholder(variable_name='chat_history', optional=True),
    ('human', '{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad', optional=True),
])

async def client_call():
    """tool to use when client visit the server"""

    #create MCP client connection
    #We usually use MultiServerMCPClient, as most of the time you need to connect many MCP servers, internally or externally
    client = MultiServerMCPClient({'my_mcp': mcp_server_config})
    #both get.tools and get_resources are async functions in the source code, must add 'await'
    #visit tools on the server
    tools = await client.get_tools()
    print(tools)

    #visit resource on the server
    resource = await client.get_resources('my_mcp', uris="datas://users/456/email")
    print(resource[0].model_dump().get('data'))

    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)

    #ainvoke: invoke in a async environment
    resp1 = await executor.ainvoke({'input': 'NBA2025年东部冠军是谁？'})
    print(resp1)


if __name__ == '__main__':
    asyncio.run(client_call())