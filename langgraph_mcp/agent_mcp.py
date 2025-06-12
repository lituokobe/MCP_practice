import asyncio
from contextlib import asynccontextmanager

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from MCP_practice.zhupu_ai import llm

mcp_server_config = {
    "url": "http://localhost:8008/sse", #defined in mcp_server.py
    "transport": "sse", #remote server only supports sse by June 2025
}

@asynccontextmanager
async def make_agent():
    """
    This is a generator, it generates an agent
    :return:
    """
    client = MultiServerMCPClient({'my_mcp': mcp_server_config})
   #create langgraph agent
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools = tools)
    yield agent

    # async with MultiServerMCPClient({'my_mcp': mcp_server_config}) as client:
    # # create langgraph agent
    #     tools = await client.get_tools()
    #     agent = create_react_agent(llm, tools=tools)
    #     # agent = create_react_agent(llm, tools=client.get_tools())
    #     yield agent


async def main():
    """
    In async environment, create an angent and execute it
    :return:
    """
    async with make_agent() as agent:
        resp = await agent.ainvoke(
            {
                "messages": [{"role": "user", "content": "2025年NBA东部冠军是什么？"}]
            }
        )
        #add await means resp must be assigned value, then continue to the next line
        #this adds a sync flavor to the async codes.
        print(resp)

if __name__ == '__main__':
    asyncio.run(main())