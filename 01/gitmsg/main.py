import typer

from analyzer.diff import get_git_diff
from analyzer.detector import detect_commit_types
from analyzer.files import get_staged_files
from ui.formatter import show_banner, show_files, show_suggestions

app = typer.Typer()

@app.command()
def generate():
    show_banner()

    diff = get_git_diff()
    files = get_staged_files()

    suggestions = detect_commit_types(diff, files)

    show_files(files)
    show_suggestions(suggestions)


@app.command()
def version():
    print("0.1.0")

if __name__ == "__main__":
    app()