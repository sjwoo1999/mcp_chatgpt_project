import asyncio
from agents.mcp import MCPServerStdio

async def main():
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "samples_dir"],
        }
    ) as server:
        print(f"🔗 서버 이름: {server.name}")
        tools = await server.list_tools()
        print("🧰 MCP tools:")
        for tool in tools:
            print(f" - {tool.name} | {tool.description or 'No description'}")

        if tools:
            result = await server.call_tool(tools[0].name, {})
            print("📦 Tool 실행 결과:")
            for item in result.content:
                print(item)

asyncio.run(main())
