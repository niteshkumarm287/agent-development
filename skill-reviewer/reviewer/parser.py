from pathlib import Path
import yaml


def find_skill_file(path: Path):
    candidates = [
        "skill.md",
        "SKILL.md"
    ]

    for file in candidates:
        skill_file = path / file

        if skill_file.exists():
            return skill_file

    return None


def load_skill(skill_path):
    metadata = {}

    metadata_file = skill_path / "metadata.yaml"

    if metadata_file.exists():
        metadata = yaml.safe_load(metadata_file.read_text())

    skill_file = find_skill_file(skill_path)

    if not skill_file:
        raise Exception(f"No skill file found in {skill_path}")

    content = skill_file.read_text()

    return {
        "metadata": metadata,
        "content": content,
        "path": str(skill_path)
    }