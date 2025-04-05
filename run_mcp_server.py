# run_mcp_server.py
from openai import OpenAI
from openai_agents.mcp import MCPServerStdio

client = OpenAI()
server = MCPServerStdio(client)
server.run()
