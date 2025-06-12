from mcp.server.fastmcp import FastMCP

from MCP_practice.zhupu_ai import zhipuai_client

mcp_server = FastMCP(name='miguel-mcp', introductions='personal mcp', port=8008)

#tool decorator from FastMCP
@mcp_server.tool('my_search_tool', description='专门搜索互联网中的内容')
def my_search(query: str) -> str:
    """搜索互联网上的内容"""
    try:
        response = zhipuai_client.web_search.web_search(
            search_engine="search-std",
            search_query=query
        )
        print(response)
        if response.search_result:
            return "\n\n".join([d.content for d in response.search_result])
    except Exception as e:
        print(e)
        return '没有搜索到任何内容！'

#define a resource to get user email, this is very similar to a tool
#except it must be exposed and accessed via an uri, and some of the input parameters is also defined in the uri
@mcp_server.resource("datas://users/{user_id}/email", name="get_user_email")
async def get_user_email(user_id: str) -> str:
    """retrieve email address from a given user id"""
    emails = {"123":"alice@example.com", "456":"bob@example.com"}
    return emails.get(user_id, "not_found@example.com")


@mcp_server.resource("datas://product-categories")
async def get_categories() -> list[str]:
    """return a list of the categories"""
    return ['electronics', 'books', 'home goods']

