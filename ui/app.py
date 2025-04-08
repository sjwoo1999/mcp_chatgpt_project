# ui/app.py

from flask import Flask, render_template, request, jsonify
import asyncio
from agents import Agent
from agents.mcp import MCPServerStdio
from agents.run_context import RunContextWrapper
from agents.run import Runner
from agents.items import ItemHelpers

app = Flask(__name__)

# MCP 서버 및 에이전트 초기화
mcp_server = MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "samples_dir"],
    },
    cache_tools_list=True
)

agent = Agent(
    name="Filesystem Agent",
    instructions="Use the tools to inspect and modify the file system.",
    mcp_servers=[mcp_server]
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_agent():
    user_input = request.json.get("input")

    async def ask():
        async with mcp_server:
            run_context = RunContextWrapper(context={})
            result = await Runner.run(
                starting_agent=agent,
                input=user_input,
                context=run_context.context
            )
            return ItemHelpers.text_message_outputs(result.new_items)

    answer = asyncio.run(ask())
    return jsonify({"response": answer})
