from MCP_practice.mcp_demo.mcp_server import mcp_server  #if you don't have parameters for name and description
 #the function name will become name, the annotation will become description
@mcp_server.tool()
def multiply(a:int, b:int) -> int:
    return a * b

@mcp_server.tool()
def add(a:int, b:int) -> int:
    return a + b