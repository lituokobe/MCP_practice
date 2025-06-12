import asyncio
import uuid
from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.constants import END
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import create_react_agent
from MCP_practice.zhupu_ai import llm


class MyState(TypedDict):
    #we have a resource to identy the email address, we want to load this resource and
    #add the identified email address to our state.
    email: str
    messages: Annotated[list, add_messages]

mcp_server_config = {
    "url": "http://localhost:8008/sse", #defined in mcp_server.py
    "transport": "sse", #remote server only supports sse by June 2025
}

def _print_event(event: dict, _printed: set, max_length=1500):
    """
    Print events

    """
    current_state = event.get("dialog_state")
    if current_state:
        print("Current state: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... and more"
            print(msg_repr)
            _printed.add(message.id)


async def async_node(state: MyState):
    """define a async node to call MCP tools"""
    print(state.get("email"))
    #  MultiServerMCPClient is from langchain_mcp_adapters.client, the instance must be created directly
    # this is different from Client from fastmcp whose instance must be created by using 'async with'
    client = MultiServerMCPClient({'my_mcp': mcp_server_config}) #related to MCP, it must be async
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools=tools)

    resp = await agent.ainvoke(state)
    return resp

async def async_resource(state: MyState):
    """define a async node to load MCP resources"""
    client = MultiServerMCPClient({'my_mcp': mcp_server_config}) #related to MCP, it must be async
    resource = await client.get_resources('my_mcp', uris="datas://users/456/email")
    return {'email':resource[0].model_dump().get('data')} #.model_dump() converts class info to a dictionary

workflow = StateGraph(MyState)
workflow.add_node('resource', async_resource) #langgraph support async function as node
workflow.add_node('agent', async_node) #langgraph support async function as node

workflow.set_entry_point('resource')
workflow.add_edge('resource','agent')
workflow.add_edge('agent', END)

#compile an async workflow
graph = workflow.compile()


#build memory
session_id = str(uuid.uuid4())
config = {
    "configurable": {
        #checkpointer is visited by thread_id
        "thread_id": session_id,
    }
}


_printed = set()

async def execute_graph():
    """execute the graph"""
    state = {"messages": []}
    while True:
        user_input = input("User: ")
        if user_input.lower() in ['quit', 'q', 'exit']:
            print("The chat is over, bye bye!")
            break
        else:
            state["messages"].append(HumanMessage(content=user_input))
            async for event in graph.astream(state, config, stream_mode="values"):
                _print_event(event, _printed)
                # Capture response and store it in memory
                response = event.get("messages", [])
                if response:
                    # Ensure response is a valid string, extracting only the content
                    response_text = response[-1].content if hasattr(response[-1], "content") else str(response[-1])
                    state["messages"].append(AIMessage(content=response_text))  # Store clean message format

if __name__ == '__main__':
    asyncio.run(execute_graph())