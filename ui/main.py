from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.before_first_request
def init_server():
    print("✅ MCP 서버 초기화 준비됨")
    path = os.path.abspath("../openai-agents-python/src/agents/mcp_filesystem_server.py")
    print(f"🔍 MCP 경로: {path}")
    if not os.path.exists(path):
        print("❌ MCP 서버 파일 없음!")
    else:
        print("✅ MCP 서버 파일 존재!")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tools")
def tools():
    return jsonify({"tools": ["list", "read", "write"]})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    tool = data.get("tool")
    try:
        path = os.path.abspath("../openai-agents-python/src/agents/mcp_filesystem_server.py")
        result = subprocess.run(
            ["python", path],
            input=tool + "\n",
            capture_output=True,
            text=True,
            timeout=10
        )
        return jsonify({"response": result.stdout})
    except Exception as e:
        return jsonify({"response": str(e)})
