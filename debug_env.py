# debug_env.py
import sys
import site

print("📦 site-packages 경로:", site.getsitepackages())
print("🧾 sys.path 확인:")
for p in sys.path:
    print(" -", p)

try:
    from openai_agents.mcp import MCPServerStdio
    print("✅ openai_agents.mcp 불러오기 성공")
except ImportError as e:
    print("❌ openai_agents.mcp 불러오기 실패:", e)
