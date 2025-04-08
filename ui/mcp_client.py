import asyncio
import os
import json

class MCPClient:
    def __init__(self, script_path: str):
        self.script_path = script_path
        self.process = None

    async def start(self):
        if not os.path.exists(self.script_path):
            raise FileNotFoundError(f"MCP script not found: {self.script_path}")

        self.process = await asyncio.create_subprocess_exec(
            "python", self.script_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

    async def send_command(self, tool: str, args: dict = {}) -> dict:
        if not self.process:
            raise RuntimeError("MCP is not running.")

        command_obj = {"tool": tool, "args": args}
        command_str = json.dumps(command_obj)

        self.process.stdin.write((command_str + "\n").encode())
        await self.process.stdin.drain()

        stdout_line = await self.process.stdout.readline()
        stderr_line = await self.process.stderr.readline()

        result = {
            "stdout": stdout_line.decode().strip(),
            "stderr": stderr_line.decode().strip()
        }

        try:
            result["parsed"] = json.loads(result["stdout"])
        except Exception:
            result["parsed"] = None

        return result
