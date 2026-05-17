def summarize_diff(diff: str):

    changes = []

    if "new file mode" in diff:
        changes.append("새로운 파일 추가")

    added_lines = sum(
        1 for line in diff.splitlines()
        if line.startswith("+") 
        and not line.startswith("+++")
    )

    if added_lines:
        changes.append(f"{added_lines} 줄 추가")
    
    return changes