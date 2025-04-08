# 📁 파일: ui/mcp_client.py

import asyncio
import os

class MCPClient:
    def __init__(self, script_path: str):
        self.script_path = script_path
        self.process = None

    async def start(self):
        if not os.path.exists(self.script_path):
            raise FileNotFoundError(f"❌ MCP 서버 스크립트가 존재하지 않음: {self.script_path}")

        self.process = await asyncio.create_subprocess_exec(
            "python", self.script_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

    async def send_command(self, command: str):
        if self.process is None:
            raise RuntimeError("MCP 서버 프로세스가 시작되지 않았습니다.")

        self.process.stdin.write((command + "\n").encode())
        await self.process.stdin.drain()

        output = await self.process.stdout.readline()
        return output.decode().strip()