# run_agent.py

import asyncio
import os
from openai_agents import Agent, MCPServerStdio
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

async def main():
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
        },
        cache_tools_list=True,
    ) as server:
        agent = Agent(
            name="ChatGPT Assistant",
            instructions="사용자의 요청에 따라 파일 시스템 도구를 사용하여 응답하세요.",
            mcp_servers=[server],
        )

        user_input = "현재 디렉토리에 있는 파일 목록을 알려줘."
        result = await agent.run(user_input)
        print("🤖 에이전트 응답:", result)

asyncio.run(main())
