def detect_commit_types(diff: str, files: list[str]):

    suggested_types = []

    # docs : 문서 수정
    if any("README" in file or file.endswith(('.md', '.rst', '.txt')) for file in files):
        suggested_types.append({
            "type": "docs",
            "reason": "문서 수정 (README, .md, .rst, .txt 파일)"
        })
    
    # test : 테스트 코드 추가
    if any("test" in file.lower() for file in files):
        suggested_types.append({
            "type": "test",
            "reason": "테스트 코드 추가"
        })
    
    # feat : 새로운 기능 추가
    if "new file mode" in diff:
        suggested_types.append({
            "type": "feat",
            "reason": "새로운 기능 추가"
        })
    
    # fix : 버그 수정
    if (
        "fix" in diff.lower() or 
        "bug" in diff.lower() or 
        "error" in diff.lower() or 
        "issue" in diff.lower()
    ):
        suggested_types.append({
            "type": "fix",
            "reason": "버그 수정"
        })
    
    # refactor : 코드 리팩토링
    if "rename" in diff.lower() or "refactor" in diff.lower():
        suggested_types.append({
            "type": "refactor",
            "reason": "코드 리팩토링"
        })
    
    # style : 코드 스타일 변경 (포맷팅, 들여쓰기 등)
    if "style" in diff.lower() or "format" in diff.lower():
        suggested_types.append({
            "type": "style",
            "reason": "코드 스타일 변경 (포맷팅, 들여쓰기 등)"
        })

    # chore : 기타 변경사항 (빌드 스크립트 수정, 패키지 매니저 설정 등)
    if not suggested_types:
        return "chore"
    
    return suggested_types