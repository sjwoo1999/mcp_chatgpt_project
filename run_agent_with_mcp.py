import asyncio
from agents import Agent
from agents.mcp import MCPServerStdio
from agents.run import Runner
from agents.run_context import RunContextWrapper
from agents.items import ItemHelpers

# MCP 서버 구성
mcp_server = MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "samples_dir"],
    },
    cache_tools_list=True
)

# Agent 구성
agent = Agent(
    name="Filesystem Agent",
    instructions="Use the tools to inspect and modify the file system.",
    mcp_servers=[mcp_server]
)

# Agent 실행
async def main():
    async with mcp_server:
        # 빈 context로 RunContextWrapper 생성
        run_context = RunContextWrapper(context={})

        # Agent 실행
        result = await Runner.run(
            starting_agent=agent,
            input="Read the contents of hello.json",
            context=run_context.context
        )

        # 출력 정리
        final_output = ItemHelpers.text_message_outputs(result.new_items)
        print(f"\n🧠 Agent Response:\n{final_output}\n")

if __name__ == "__main__":
    asyncio.run(main())
