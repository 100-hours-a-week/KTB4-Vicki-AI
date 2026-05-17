from rich.console import Console
from rich.panel import Panel

console = Console()

def show_banner():
    console.print(
        Panel(
            "[bold cyan]Git Commit Type Suggester[/bold cyan]\n"
            "자동으로 커밋 타입을 제안하는 도구",
            title="[bold magenta]Welcome![/bold magenta]",
            border_style="cyan"
        )
    )

def show_files(files: list[str]):
    console.print(
        "[bold yellow]Detected Files[/bold yellow]"
    )
    for file in files:
        console.print(f"- {file}")

def show_suggestions(suggestions):
    console.print(
        "[bold yellow]Suggested Commit Type(s):[/bold yellow]"
    )
    for idx, suggestion in enumerate(suggestions, start=1):
        console.print(
            f"[bold green]{suggestion['type']}[/bold green] : {suggestion['reason']}"
        )