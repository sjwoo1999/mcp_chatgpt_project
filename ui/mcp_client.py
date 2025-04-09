import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# MCP 서버와 통신하는 비동기 클라이언트
class MCPClient:
    def __init__(self, command: str, cwd: str, env: dict):
        self.command = command
        self.cwd = cwd
        self.env = env
        self.session: ClientSession | None = None

    async def connect(self):
        try:
            params = StdioServerParameters(
                command=self.command,
                args=[],
                env=self.env,
                cwd=self.cwd,
                encoding="utf-8"
            )
            read, write = await stdio_client(params)
            self.session = await ClientSession(read, write).__aenter__()
            print("✅ MCPClient 연결 성공")
        except Exception as e:
            print(f"❌ MCPClient 연결 실패: {e}")
            raise

    async def call(self, tool_name: str, arguments: dict):
        if not self.session:
            raise RuntimeError("MCP client not connected.")
        try:
            return await self.session.call_tool(tool_name, arguments)
        except Exception as e:
            print(f"❌ MCPClient 호출 중 에러: {e}")
            return {"error": str(e)}

    async def close(self):
        if self.session:
            try:
                await self.session.__aexit__(None, None, None)
                print("📴 MCPClient 연결 종료됨")
            except Exception as e:
                print(f"⚠️ MCPClient 종료 중 에러: {e}")
