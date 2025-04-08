# ui/mcp_client.py
import asyncio
import os
import subprocess

class MCPClient:
    def __init__(self, script_path: str):
        self.script_path = script_path
        self.process = None

    async def start(self):
        self.process = await asyncio.create_subprocess_exec(
            "python", self.script_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

    async def send_command(self, command: str):
        self.process.stdin.write((command + "\n").encode())
        await self.process.stdin.drain()

        output = await self.process.stdout.readline()
        return output.decode().strip()
