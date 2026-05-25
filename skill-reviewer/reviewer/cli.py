from pathlib import Path
import typer
from rich import print
from rich.table import Table

from reviewer.parser import load_skill
from reviewer.validator import validate_skill
from reviewer.ai_reviewer import review_with_ai
from reviewer.scorer import calculate_score

app = typer.Typer()


REQUIRED_FILES = [
    "metadata.yaml",
    "skill.md"
]


def is_skill_directory(path: Path):
    if not path.is_dir():
        return False

    skill_files = [
        "skill.md",
        "SKILL.md"
    ]

    for file in skill_files:
        if (path / file).exists():
            return True

    return False


@app.command()
def scan(path: str):
    target = Path(path)

    if not target.exists():
        print(f"[red]Path does not exist:[/red] {path}")
        raise typer.Exit(code=1)

    skill_directories = []

    # Direct skill file
    if target.is_file() and target.name.lower() == "skill.md":
        skill_directories.append(target.parent)
    
    # Single skill directory
    elif is_skill_directory(target):
        skill_directories.append(target)
    
    # Parent directory containing multiple skills
    elif target.is_dir():
        for item in target.iterdir():
            if item.is_dir() and is_skill_directory(item):
                skill_directories.append(item)

    if not skill_directories:
        print("[yellow]No valid skills found[/yellow]")
        raise typer.Exit(code=0)

    table = Table(title="Skill Review Report")

    table.add_column("Skill")
    table.add_column("Score")
    table.add_column("Status")
    table.add_column("Issues")

    for skill_dir in skill_directories:
        skill = load_skill(skill_dir)

        issues = validate_skill(skill)

        ai_review = review_with_ai(skill["content"])

        score = calculate_score(issues, ai_review)

        status = "PASS" if score >= 70 else "WARN"

        issues_text = "None"
        if issues:
            issues_text = " | ".join(issues)

        table.add_row(
            skill_dir.name,
            f"{score}/100",
            status,
            issues_text
        )

    print(table)


if __name__ == "__main__":
    app()