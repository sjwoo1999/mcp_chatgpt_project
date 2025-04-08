# 📁 파일: ui/main.py

from flask import Flask, render_template, request, jsonify
import os
import asyncio
from ui.mcp_client import MCPClient  # ✅ subprocess -> MCPClient 사용으로 변경

app = Flask(__name__)

# 🔁 비동기 루프 전역 생성
loop = asyncio.get_event_loop()

# 📌 MCPClient 전역 객체 초기화
mcp_client = None

@app.before_first_request
def init_server():
    global mcp_client
    print("\n✅ MCP 서버 초기화 준비됨")
    path = os.path.abspath("../openai-agents-python/src/agents/mcp_filesystem_server.py")
    print(f"🔍 MCP 경로: {path}")
    if not os.path.exists(path):
        print("❌ MCP 서버 파일 없음!")
    else:
        print("✅ MCP 서버 파일 존재!")
        mcp_client = MCPClient(path)
        loop.run_until_complete(mcp_client.start())  # 🧠 비동기 서버 실행 유지

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tools")
def tools():
    return jsonify({"tools": ["list", "read", "write"]})

@app.route("/ask", methods=["POST"])
def ask():
    global mcp_client
    data = request.get_json()
    tool = data.get("tool")

    # 📦 명령어 구체화 (작업 3)
    if tool == "list":
        command = "list"
    elif tool == "read":
        command = "read samples_dir/hello.json"
    elif tool == "write":
        command = "write samples_dir/hello.json {\"msg\": \"Hi!\"}"
    else:
        return jsonify({"response": "❌ Unknown tool.", "error": True})

    # 🧪 MCPClient 비동기 커맨드 실행
    try:
        result = loop.run_until_complete(mcp_client.send_command(command))
        return jsonify({"response": result, "error": False})
    except Exception as e:
        return jsonify({"response": f"❌ 오류: {str(e)}", "error": True})
    
# 📁 파일: ui/main.py (`init_server()`에 추가)

@app.route("/server-status")
def server_status():
    path = os.path.abspath("../openai-agents-python/src/agents/mcp_filesystem_server.py")
    return jsonify({"exists": os.path.exists(path)})