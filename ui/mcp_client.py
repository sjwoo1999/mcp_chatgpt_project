# 📁 파일: ui/mcp_client.py

import asyncio
import os
import sys
import importlib.util

class MCPClient:
    def __init__(self, script_path: str):
        self.script_path = script_path
        self.process = None

    async def start(self):
        if not os.path.exists(self.script_path):
            raise FileNotFoundError(f"❌ MCP 서버 스크립트가 존재하지 않음: {self.script_path}")

        self._ensure_openai_installed()

        # ✅ PYTHONPATH 설정
        pythonpath = os.path.abspath("../openai-agents-python/src")
        env = os.environ.copy()
        env["PYTHONPATH"] = pythonpath

        print(f"🔧 MCP subprocess PYTHONPATH = {pythonpath}")

        self.process = await asyncio.create_subprocess_exec(
            "python", self.script_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env  # ✅ 환경 변수 주입
        )

        asyncio.create_task(self._read_stderr())

    async def _read_stderr(self):
        while True:
            line = await self.process.stderr.readline()
            if not line:
                break
            print(f"🪵 STDERR | {line.decode().strip()}")

    async def send_command(self, command: str) -> str:
        if self.process is None:
            raise RuntimeError("MCP 서버 프로세스가 시작되지 않았습니다.")

        self.process.stdin.write((command + "\n").encode())
        await self.process.stdin.drain()

        output = await self.process.stdout.readline()
        return output.decode().strip()

    def _ensure_openai_installed(self):
        if importlib.util.find_spec("openai") is None:
            raise ImportError("❌ MCP 서버는 'openai' 모듈이 필요합니다. 먼저 설치하세요: pip install openai")
