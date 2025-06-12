import asyncio

from fastmcp import Client
from fastmcp.client import SSETransport

mcp_server_config = {
    "url": "http://localhost:8008/sse", #defined in mcp_server.py
    "transport": "sse", #remote server only supports sse by June 2025
}

async def test_client():
    """user fastmcp client to call tools"""
    #Client is from fastmcp, the instance must be created by using 'async with', otherwise there will be an error
    #This is different from MultiServerMCPClient from langchain_mcp_adapters.client
    async with Client(SSETransport(url = "http://localhost:8008/sse")) as client:
        tools = await client.list_tools()
        print(tools)
        resource = await client.list_resources()
        print(resource)

        email = await client.read_resource('datas://users/456/email')
        print(email)

        product_cat = await client.read_resource("datas://product-categories")
        print(product_cat[0].text.split('\n')[1])

        #call one of the tools
        result = await client.call_tool(name = 'minus', arguments= {"a":34, "b":12})
        print(result)

if __name__ == '__main__':
    asyncio.run(test_client())