# 🚀 MCP Practice Repository  

## 📌 Overview  
This repository serves as a **hands-on practice** for **MCP**, utilizing **LangChain** and **FastMCP** libraries. The projects focus on **tool calling**, **agent-based interactions**, and **LLM-powered searches**.  

---

## 🗂 Repository Structure  

### 🔹 **Function Calling (`./FC`)**  
- `fc_demo.py`: Simulates a weather-checking tool called via LLM, replicating tool calling methods from 2023. In 2025, we shift to agent-based interactions.  
- `fc_demo2.py`: Implements GLM's search function for LLM-based weather queries, optimized for Chinese language support.  
- `fc_demo3.py`: Demonstrates GLM’s LLM model search capability using GLM's demo code.  

### 🔹 **Agent-Based AI (`./agent_demo`)**  
- `zhipu_demo.py`: Uses **Zhipu LLM + LangChain** to build a quick AI chat/search bot with memory.  

### 🔹 **MCP Server & Clients (`./mcp_demo`)**  
- `mcp_server.py`: Implements an MCP server with one search tool and two resources (runs on local port 8008).  
- `main.py`: Launches the MCP server.  
- `agent_client.py`: Creates a simple chatbot using MCP tools in LangChain.  
- `fastmcp_client.py`: Builds a FastMCP-based chatbot.  

### 🔹 **LangGraph MCP Agents (`./langgraph_mcp`)**  
- `agent_mcp.py`: Develops a basic asynchronous agent to call MCP tools via **LangGraph**.  
- `graph_mcp.py`: Constructs a two-node async chatbot using LangGraph, capable of interacting with MCP tools and resources.  

