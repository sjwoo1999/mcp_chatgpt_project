# 📁 파일: ui/mcp_client.py

import asyncio
import os
import importlib.util

class MCPClient:
    def __init__(self, script_path: str):
        self.script_path = script_path
        self.process = None

    async def start(self):
        # ✅ openai 모듈 설치 여부 사전 확인
        self._ensure_openai_installed()

        if not os.path.exists(self.script_path):
            raise FileNotFoundError(f"❌ MCP 서버 스크립트가 존재하지 않음: {self.script_path}")

        # 🧠 subprocess 실행 (stdin/stdout/stderr 파이프 설정)
        self.process = await asyncio.create_subprocess_exec(
            "python", self.script_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # 🔍 stderr 로그 비동기 감시 시작
        asyncio.create_task(self._read_stderr())

    def _ensure_openai_installed(self):
        # 🧪 openai 모듈이 현재 Python 환경에 설치되어 있는지 확인
        if importlib.util.find_spec("openai") is None:
            raise RuntimeError(
                "❌ openai 모듈이 설치되어 있지 않습니다. `pip install openai` 먼저 실행하세요."
            )

    async def _read_stderr(self):
        # 📡 stderr 로그 실시간 출력
        while True:
            line = await self.process.stderr.readline()
            if not line:
                break
            print(f"🪵 STDERR | {line.decode().strip()}")

    async def send_command(self, command: str) -> str:
        if self.process is None:
            raise RuntimeError("MCP 서버 프로세스가 시작되지 않았습니다.")

        # ✉️ 명령어 전송
        self.process.stdin.write((command + "\n").encode())
        await self.process.stdin.drain()

        # 📥 응답 수신
        response = await self.process.stdout.readline()
        return response.decode().strip()