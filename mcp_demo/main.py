from MCP_practice.mcp_demo.mcp_server import mcp_server
import MCP_practice.mcp_demo.mcp_tools

if __name__ == '__main__':
    mcp_server.run(transport = 'sse')