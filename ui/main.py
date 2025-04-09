# 📁 ui/main.py

from flask import Flask, render_template, request, jsonify
import asyncio
import os
from ui.mcp_client import MCPClient

app = Flask(__name__)

# ✅ MCP 서버 실행에 필요한 설정 값
MCP_SERVER_COMMAND = "python"
MCP_SERVER_CWD = os.path.abspath(os.path.join(os.path.dirname(__file__), "../openai-agents-python/src/agents/mcp"))
MCP_SERVER_ENV = {"PYTHONPATH": os.path.abspath(os.path.join(os.path.dirname(__file__), "../openai-agents-python/src"))}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    tool_name = data.get("tool") or "list"  # 기본값
    arguments = data.get("args") or {}

    async def call():
        client = MCPClient(command=MCP_SERVER_COMMAND, cwd=MCP_SERVER_CWD, env=MCP_SERVER_ENV)
        await client.connect()
        result = await client.call(tool_name, arguments)
        await client.close()
        return result

    result = asyncio.run(call())
    return jsonify(result)

# ✨ MCP 서버 파일 여부 확인을 위한 endpoint
@app.route("/server-status", methods=["GET"])
def server_status():
    mcp_server_path = os.path.join(MCP_SERVER_CWD, "mcp_filesystem_server.py")
    exists = os.path.exists(mcp_server_path)
    return jsonify({"exists": exists})