# 🔧 수정 완료된 main.py (Flask + MCP 비동기 통합)

import os
import sys
import asyncio
import nest_asyncio
from flask import Flask, render_template, request, jsonify

# 🧠 1. PYTHONPATH 설정을 위해 루트 디렉토리 삽입
CURRENT_FILE = os.path.abspath(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_FILE, "../.."))
if ROOT_DIR not in sys.path:
    print("📂 sys.path에 프로젝트 루트 추가:", ROOT_DIR)
    sys.path.insert(0, ROOT_DIR)

# 🔄 2. 루트 설정 후 내부 모듈 import
from ui.mcp_client import MCPClient

# 🌀 3. 이벤트 루프 중첩 허용 (Flask + asyncio 공존)
nest_asyncio.apply()
app = Flask(__name__)
mcp_client: MCPClient | None = None

# 🛠 4. MCP 파일 경로 지정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MCP_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../openai-agents-python/src/agents/mcp/mcp_filesystem_server.py")
)

# ✅ 5. MCP 서버 비동기 초기화 함수
async def start_mcp():
    global mcp_client
    print("✅ MCP 서버 초기화 준비됨")
    print(f"🔍 MCP 경로: {MCP_PATH}")

    if not os.path.exists(MCP_PATH):
        print("❌ MCP 서버 파일 없음")
        return

    try:
        mcp_client = MCPClient(MCP_PATH)
        await mcp_client.start()
        print("🚀 MCP subprocess 시작 완료")
    except Exception as e:
        print(f"❌ MCP 시작 중 예외 발생: {e}")

# 🔁 6. Flask + Asyncio 병합 실행기
def start_flask_with_async():
    import threading

    def run_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_mcp())
        loop.run_forever()

    threading.Thread(target=run_loop, daemon=True).start()
    app.run(debug=True)

# 🌐 7. Flask 라우트 정의
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
async def ask():
    global mcp_client
    if not mcp_client or not mcp_client.process:
        return jsonify({"response": "❌ MCP 서버 프로세스가 초기화되지 않았습니다.", "error": True})

    data = request.get_json()
    tool = data.get("tool")

    if tool == "list":
        command = "list"
    elif tool == "read":
        command = 'read {"path": "hello.json"}'
    elif tool == "write":
        command = 'write {"path": "hello.json", "content": "Hi"}'
    else:
        return jsonify({"response": "❌ Unknown tool", "error": True})

    try:
        result = await mcp_client.send_command(command)
        return jsonify({"response": result, "error": False})
    except Exception as e:
        return jsonify({"response": f"❌ MCP 실행 중 오류: {str(e)}", "error": True})

@app.route("/server-status")
def server_status():
    return jsonify({"exists": os.path.exists(MCP_PATH)})

# ▶️ 8. 앱 실행 시작
if __name__ == "__main__":
    start_flask_with_async()
