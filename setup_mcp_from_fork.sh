from pathlib import Path

# Create a shell script to automate the MCP fork + integration setup
script_path = Path("/mnt/data/setup_mcp_from_fork.sh")

script_content = """#!/bin/bash

set -e

echo "📦 Step 1: Backing up existing openai-agents-python..."
cp -r mcp_chatgpt_project/openai-agents-python mcp_chatgpt_project/openai-agents-python-backup

echo "🧹 Step 2: Removing old directory..."
rm -rf mcp_chatgpt_project/openai-agents-python

echo "🌐 Step 3: Cloning your forked repo..."
git clone https://github.com/sjwoo1999/openai-agents-python.git mcp_chatgpt_project/openai-agents-python

echo "🔧 Step 4: Applying custom changes from backup..."
cp -r mcp_chatgpt_project/openai-agents-python-backup/src/agents/mcp/* mcp_chatgpt_project/openai-agents-python/src/agents/mcp/

echo "✅ Step 5: Checking git status inside forked directory..."
cd mcp_chatgpt_project/openai-agents-python
git status

echo "💾 Step 6: Committing your custom changes..."
git add .
git commit -m "✨ Custom: Applied local MCP modifications"
git push origin main

echo "🔁 Step 7: Adding upstream for future updates..."
git remote add upstream https://github.com/openai/openai-agents.git
git fetch upstream

echo "✅ Done! Your fork is now updated with your custom MCP changes and ready for integration."
"""

script_path.write_text(script_content)
script_path.chmod(0o755)

script_path
