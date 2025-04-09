🧠 MCP ChatGPT Project
로컬에서 실행 가능한 MCP Tool Server와 이를 사용하는 Flask UI 클라이언트가 통합된 프로젝트입니다.

📦 프로젝트 구조

```
. ├── ui/ # Flask 프론트엔드
│ ├── main.py # Flask 웹 서버
│ ├── mcp_client.py # MCP 통신 클라이언트
│ ├── templates/index.html # 웹 UI
│ └── static/style.css # 스타일 시트
├── openai-agents-python/
│ └── src/agents/
│ ├── tools/filesystem_tool.py # MCP Tool 정의
│ └── mcp/mcp_filesystem_server.py # MCP Tool Server
├── samples_dir/ # list/read/write용 테스트 파일 저장소
├── setup_mcp.sh # MCP 서버 실행 스크립트 └── README.md # 이 문서
```

🚀 실행 방법
1. MCP 서버 실행
``` chmod +x setup_mcp.sh ./setup_mcp.sh ```

MCP Tool 서버는 python openai-agents-python/src/agents/mcp/mcp_filesystem_server.py를 실행하며,
stdin/stdout 기반으로 MCP Tool 요청을 처리합니다.

2. Flask 앱 실행
``` cd ui flask run ```

기본 주소: http://127.0.0.1:5000

3. 웹 페이지 사용

- list: samples_dir의 파일 목록

- read: 파일 경로 입력 시 파일 읽기

- write: 파일 경로 + 내용 입력 후 쓰기

🛠 MCP Tool 설명

- list: samples_dir의 파일 목록 반환

- read(path: str): 지정된 파일 내용 반환

- write(path: str, content: str): 파일에 내용 저장 후 결과 메시지 반환

📂 예제 디렉토리 구성

```
samples_dir/
├── example1.txt # 읽기용 샘플
├── example2.txt # 수정용 샘플
```

✅ 의존성 설치
```
pip install -r requirements.txt
```

mcp, flask, anyio 등 필요 패키지 포함