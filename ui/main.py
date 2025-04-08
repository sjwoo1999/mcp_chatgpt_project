from flask import Flask, render_template, request, jsonify
import os
from mcp_client import MCPClient

app = Flask(__name__)
client = None

@app.before_first_request
def init_server():
    global client
    print("✅ MCP 서버 초기화 준비됨")
    path = os.path.abspath("openai-agents-python/src/agents/mcp_filesystem_server.py")
    print(f"🔍 MCP 경로: {path}")
    if not os.path.exists(path):
        print("❌ MCP 서버 파일 없음!")
    else:
        print("✅ MCP 서버 파일 존재!")
        client = MCPClient(script_path=path)
        import asyncio
        asyncio.get_event_loop().create_task(client.start())

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tools")
def tools():
    return jsonify({"tools": ["list", "read", "write"]})

@app.route("/ask", methods=["POST"])
async def ask():
    global client
    data = request.get_json()
    tool = data.get("tool", "")
    try:
        if client is None:
            return jsonify({"response": "MCPClient not initialized"})
        output = await client.send_command(tool)
        return jsonify({"response": output})
    except Exception as e:
        return jsonify({"response": f"오류: {str(e)}"})
