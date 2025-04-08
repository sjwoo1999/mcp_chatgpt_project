import asyncio
from flask import Flask, render_template, request, jsonify

from agents import Agent
from agents.mcp import MCPServerStdio

app = Flask(__name__)

# MCP 서버 구성
mcp_server = MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "samples_dir"],
    },
    cache_tools_list=True
)

# 에이전트 설정 (에러의 핵심 fix: name, instructions 추가)
agent = Agent(
    name="파일 시스템 에이전트",
    instructions="MCP 툴을 사용해 파일을 읽고 쓰세요.",
    mcp_servers=[mcp_server]
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("input", "")
    
    async def run_agent():
        async with mcp_server:
            return await agent.run(user_input)

    result = asyncio.run(run_agent())
    return jsonify({"response": result})
