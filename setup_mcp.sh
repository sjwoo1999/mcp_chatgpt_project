#!/bin/bash
echo "🚀 MCP 서버 시작..."
python openai-agents-python/src/agents/mcp/mcp_filesystem_server.py &

echo "🌐 Flask 서버 실행..."
export FLASK_APP=ui/main.py
export FLASK_ENV=development
export PYTHONPATH=.:./openai-agents-python/src
flask run