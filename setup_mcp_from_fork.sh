#!/bin/bash

set -e

echo "📦 Step 1: 기존 openai-agents-python 백업 중..."
cp -r openai-agents-python openai-agents-python-backup

echo "🧹 Step 2: 기존 openai-agents-python 디렉토리 제거 중..."
rm -rf openai-agents-python

echo "🌐 Step 3: Fork된 최신 리포지토리 클론 중..."
git clone https://github.com/sjwoo1999/openai-agents-python.git openai-agents-python

echo "🔧 Step 4: 백업본에서 수정된 MCP 파일 복원 중..."
cp -r openai-agents-python-backup/src/agents/mcp/* openai-agents-python/src/agents/mcp/

echo "✅ Step 5: Git 상태 확인 중..."
cd openai-agents-python
git status

echo "💾 Step 6: 변경사항 커밋 및 푸시 중..."
git add .
git commit -m '✨ Custom: Applied local MCP modifications' || echo "⚠️ 커밋할 변경사항 없음"
git push origin main

echo "🔁 Step 7: upstream 등록 및 fetch 중..."
git remote remove upstream 2>/dev/null || true
git remote add upstream https://github.com/openai/openai-agents-python.git
git fetch upstream

echo "🧼 Step 8: 백업 폴더 삭제 중..."
cd ..
rm -rf openai-agents-python-backup

echo "🎉 완료! Fork 리포에 수정사항 반영됨 + 백업 제거 완료 ✅"
