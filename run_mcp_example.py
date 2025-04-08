import asyncio
from agents.mcp import MCPServerStdio

async def main():
    # 1. MCP 서버 초기화
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "samples_dir"],
        },
        cache_tools_list=True
    ) as server:
        print(f"🔗 서버 이름: {server.name}")

        # 2. 사용 가능한 툴 출력
        tools = await server.list_tools()
        print("🧰 MCP tools:")
        for tool in tools:
            print(f" - {tool.name} | {tool.description or 'No description'}")

        # 3. 'read_file' tool 실행
        result = await server.call_tool("read_file", {
            "path": "samples_dir/hello.json"
        })

        # 4. 결과 출력
        print("📦 Tool 실행 결과:")
        for item in result.content:
            print(f"🔹 type={item.type} | text={item.text}")

asyncio.run(main())
