# 1주차 과제
1. CLI 프로그램 만들기
2. CLI 비동기 처리가 가능해 보이는 것을 리팩토링 (선택)

# 프로그램 개요
### 프로젝트 이름
Git Commit Message Generator

### Overview
Git Staged changes를 분석하여
Conventional Commit 기반의 commit type을 추천하는 CLI 프로그램

현재는 rule-based 방식으로 동작하며,
변경된 파일과 diff 내용을 기반으로 commit type을 추천합니다.

### Features
- Git staged diff 분석
- 변경된 파일 목록 분석
- Conventional Commit type 추천
- 추천 이유 출력
- Rich 기반 CLI UI 제공

### 설치방법
```
git clone <repo_url>

cd gitmsg

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

### 사용방법
먼저 작업중인 Git 프로젝트에서 변경사항을 staging 합니다
이후 Git 프로젝트 디렉토리에서 아래 명령어를 실행합니다.
```
puthon3 {gitmsg_프로젝트_경로}/main.py generate
```


### 프로젝트 구조
gitmsg/
│
├── analyzer/
│   ├── diff.py
│   ├── files.py
│   └── detector.py
│
├── ui/
│   └── formatter.py
│
├── main.py
├── requirements.txt
└── README.md

### 추후 개선방향
- commit message 제목 자동 생성
- AI 기반 commit message 생성