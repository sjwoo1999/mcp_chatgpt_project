import sys
import os

# 'src' 폴더를 Python 모듈 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

try:
    # 실제 존재하는 MCP 관련 클래스들 중 하나 이상을 임포트
    from agents.mcp import MCPServerStdio, MCPUtil
    print("✅ agents.mcp 임포트 성공!")
except ImportError as e:
    print("❌ agents.mcp 임포트 오류:", e)

try:
    import openai
    print(f"✅ openai 임포트 성공! 버전: {openai.__version__}")
except ImportError as e:
    print("❌ openai 임포트 오류:", e)
