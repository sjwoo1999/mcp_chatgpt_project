# 📁 파일: ui/mcp_client.py

import asyncio
import os
import importlib.util

class MCPClient:
    def __init__(self, script_path: str):
        self.script_path = script_path
        self.process = None

    async def start(self):
        self._ensure_openai_installed()

        # ✅ 경로 정확히 지정
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        base_path = os.path.join(project_root, "openai-agents-python", "src")

        if not os.path.exists(base_path):
            raise FileNotFoundError(f"❌ base_path 디렉토리가 존재하지 않습니다: {base_path}")

        env = os.environ.copy()
        env["PYTHONPATH"] = base_path
        print(f"🔧 MCP subprocess PYTHONPATH = {base_path}")

        # ✅ 핵심: mcp_filesystem_server.py를 -m 모듈 실행 방식으로 바꿈
        self.process = await asyncio.create_subprocess_exec(
            "python", "-m", "agents.mcp.mcp_filesystem_server",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            cwd=base_path  # ✅ 여기가 PYTHONPATH의 시작점
        )

        print("🚀 MCP subprocess 실행 완료")
        asyncio.create_task(self._read_stderr())

    async def _read_stderr(self):
        try:
            while True:
                line = await self.process.stderr.readline()
                if not line:
                    break
                print(f"🪵 STDERR | {line.decode().strip()}")
        except Exception as e:
            print(f"❌ STDERR 읽기 중 오류: {str(e)}")

    async def send_command(self, command: str) -> str:
        if self.process is None or self.process.stdin is None:
            raise RuntimeError("❌ MCP 서버 프로세스가 초기화되지 않았습니다.")

        if self.process.returncode is not None:
            raise RuntimeError("❌ MCP subprocess가 종료되었습니다.")

        try:
            self.process.stdin.write((command + "\n").encode())
            await self.process.stdin.drain()
        except (BrokenPipeError, ValueError) as pipe_err:
            raise RuntimeError(f"❌ MCP pipe 쓰기 오류: {str(pipe_err)}")

        try:
            output = await self.process.stdout.readline()
            if not output:
                raise RuntimeError("❌ MCP subprocess에서 응답이 없습니다.")
            return output.decode().strip()
        except Exception as read_err:
            raise RuntimeError(f"❌ MCP 응답 수신 중 오류: {str(read_err)}")

    def _ensure_openai_installed(self):
        if importlib.util.find_spec("openai") is None:
            raise ImportError("❌ MCP 서버는 'openai' 모듈이 필요합니다. pip install openai 로 설치하세요.")
