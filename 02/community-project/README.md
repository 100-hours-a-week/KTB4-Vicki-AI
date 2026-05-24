# 프로젝트 개요
FastAPI로 만든 커뮤니티 서비스 백엔드

# 프로젝트 구조
```
├── main.py
├── database.py    # engine, db 생성
├── models.py      # sqlalchemy 테이블과 매핑
├── schemas.py     # pydantic validation
├── routers
│   ├── comments.py
│   ├── posts.py
│   └── users.py
├── services
│   ├── comments.py
│   ├── posts.py
│   ├── users.py
│   └── ai_service.py
├── repositories
│   ├── comments.py
│   ├── posts.py
│   └── users.py
└── README.md
```

# API 명세서 및 DDL
[노션 링크](https://www.notion.so/2-36806f054233803a8cdbf573efea95c2?source=copy_link)

# 회고
