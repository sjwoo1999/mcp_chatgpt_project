# ✅ main.py – Flask + MCPClient 통합 컨트롤러
from flask import Flask, render_template, request, jsonify
import os
import asyncio

# 🧠 커스텀 MCPClient (subprocess + async 통신)
from ui.mcp_client import MCPClient

# 🏗 Flask App 생성
app = Flask(__name__)

# 🔁 전역 이벤트 루프 – 단 한 번 생성, 반복 재사용
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 📦 MCPClient 인스턴스 – 서버 시작 전 전역 선언
mcp_client = None

# 📌 MCP 서버 실행 스크립트 경로 설정 (절대경로로 안정성 확보)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MCP_PATH = os.path.abspath(os.path.join(BASE_DIR, "../openai-agents-python/src/agents/mcp/mcp_filesystem_server.py"))

@app.before_first_request
def init_server():
    """🌐 Flask 앱 최초 요청 전에 MCP subprocess 서버 실행"""
    global mcp_client

    print("\n✅ MCP 서버 초기화 준비됨")
    print(f"🔍 MCP 경로: {MCP_PATH}")

    if not os.path.exists(MCP_PATH):
        print("❌ MCP 서버 파일 없음!")
        return

    print("✅ MCP 서버 파일 존재!")
    mcp_client = MCPClient(MCP_PATH)

    try:
        result = loop.run_until_complete(mcp_client.send_command(command))
        return jsonify({"response": result, "error": False})
    except:
        error_msg = str(e)
        if asyncio.iscoroutine(e):
            error_msg = loop.run_until_complete(e) # 🧠 비동기 예외 객체면 실행해서 메시지 추출
        return jsonify({"response": f"❌ MCP 실행 중 오류: {error_msg}", "error": True})

@app.route("/")
def home():
    """🏠 메인 페이지 라우팅"""
    return render_template("index.html")

@app.route("/tools")
def tools():
    """🧰 사용 가능한 MCP 도구 목록"""
    return jsonify({"tools": ["list", "read", "write"]})

@app.route("/ask", methods=["POST"])
def ask():
    """📨 사용자가 버튼으로 MCP 도구 요청"""
    global mcp_client

    if mcp_client is None:
        return jsonify({"response": "❌ MCP 서버가 아직 시작되지 않았습니다.", "error": True})

    data = request.get_json()
    tool = data.get("tool")

    # 🧩 명령어 파싱
    if tool == "list":
        command = "list"
    elif tool == "read":
        command = "read samples_dir/hello.json"
    elif tool == "write":
        command = "write samples_dir/hello.json {\"msg\": \"Hi!\"}"
    else:
        return jsonify({"response": "❌ 알 수 없는 도구 요청", "error": True})

    # 🧪 subprocess에 명령 전송 → 응답 반환
    try:
        result = loop.run_until_complete(mcp_client.send_command(command))
        return jsonify({"response": result, "error": False})
    except Exception as e:
        return jsonify({"response": f"❌ MCP 실행 중 오류: {str(e)}", "error": True})

@app.route("/server-status")
def server_status():
    """🔍 MCP 서버 파일 존재 여부 확인용"""
    return jsonify({"exists": os.path.exists(MCP_PATH)})
