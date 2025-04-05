import sys
print("[sys.path]", sys.path)

try:
    from agents.mcp import MCPServerStdio
    print("MCPServerStdio 임포트 성공!")
except ImportError as e:
    print("임포트 오류:", e)

try:
    import openai
    print("openai 임포트 성공!")
except ImportError as e:
    print("openai 임포트 오류:", e)
