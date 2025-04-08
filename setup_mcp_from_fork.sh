#!/bin/bash

set -e

echo "📦 Step 1: Backing up existing openai-agents-python..."
cp -r openai-agents-python openai-agents-python-backup

echo "🧹 Step 2: Removing old directory..."
rm -rf openai-agents-python

echo "🌐 Step 3: Cloning your forked repo..."
git clone https://github.com/sjwoo1999/openai-agents-python.git openai-agents-python

echo "🔧 Step 4: Applying custom changes from backup..."
cp -r openai-agents-python-backup/src/agents/mcp/* openai-agents-python/src/agents/mcp/

echo "✅ Step 5: Checking git status inside forked directory..."
cd openai-agents-python
git status

echo "💾 Step 6: Committing your custom changes..."
git add .
git commit -m '✨ Custom: Applied local MCP modifications'
git push origin main

echo "🔁 Step 7: Adding upstream for future updates..."
git remote remove upstream 2>/dev/null || true
git remote add upstream https://github.com/openai/openai-agents-python.git
git fetch upstream

echo "✅ Done! Your fork is now updated with your custom MCP changes and ready for integration."
