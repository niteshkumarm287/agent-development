import os
import subprocess
import vertexai
from vertexai.generative_models import GenerativeModel
from datetime import date

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "game-d8160")
REGION     = os.environ.get("GCP_REGION", "us-central1")

vertexai.init(project=PROJECT_ID, location=REGION)
model = GenerativeModel("gemini-2.5-flash")

def get_git_log(from_ref: str = "", to_ref: str = "HEAD") -> str:
    """Returns structured git log between two refs."""
    ref_range = f"{from_ref}..{to_ref}" if from_ref else to_ref
    cmd = [
        "git", "log", ref_range,
        "--pretty=format:%H|%s|%an|%ad",
        "--date=short",
        "--no-merges",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"git log failed: {result.stderr}")
    return result.stdout.strip()

def get_latest_tag() -> str:
    """Returns the most recent git tag, or empty string if none."""
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else ""

def parse_commits(raw_log: str) -> dict:
    """Groups commits by Conventional Commits type."""
    groups = {
        "feat":     [],
        "fix":      [],
        "docs":     [],
        "chore":    [],
        "refactor": [],
        "perf":     [],
        "test":     [],
        "other":    [],
    }
    for line in raw_log.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 3)
        if len(parts) < 2:
            continue
        sha, subject = parts[0][:8], parts[1]
        author = parts[2] if len(parts) > 2 else ""

        matched = False
        for prefix in groups:
            if subject.lower().startswith(f"{prefix}:") or \
               subject.lower().startswith(f"{prefix}("):
                groups[prefix].append(f"{sha} {subject} ({author})")
                matched = True
                break
        if not matched:
            groups["other"].append(f"{sha} {subject} ({author})")

    return {k: v for k, v in groups.items() if v}

def generate_changelog(
    version: str,
    from_ref: str = "",
    to_ref: str = "HEAD",
    repo_path: str = ".",
) -> str:
    orig_dir = os.getcwd()
    os.chdir(repo_path)

    try:
        if not from_ref:
            from_ref = get_latest_tag()

        raw_log = get_git_log(from_ref, to_ref)
        if not raw_log:
            return f"## [{version}] — {date.today()}\n\nNo changes found.\n"

        grouped = parse_commits(raw_log)

        commit_summary = ""
        for group, commits in grouped.items():
            commit_summary += f"\n### {group}\n"
            for c in commits:
                commit_summary += f"- {c}\n"

        prompt = f"""You are a technical writer generating a changelog entry.
Convert these git commits into a clean, human-readable changelog section.

Follow Keep a Changelog format (https://keepachangelog.com).
Use these section headings where relevant:
Added, Changed, Deprecated, Removed, Fixed, Security

Version: {version}
Date: {date.today()}
Commits grouped by type:
{commit_summary}

Rules:
- Rewrite commit messages into clear user-facing descriptions
- Group related commits into single entries where sensible
- Drop trivial commits (bump version, fix typo in test, etc.)
- Start the output with ## [{version}] — {date.today()}
- Return only the markdown changelog section, no preamble"""

        response = model.generate_content(prompt)
        return response.text

    finally:
        os.chdir(orig_dir)

def prepend_to_changelog(new_section: str, changelog_path: str = "CHANGELOG.md"):
    """Prepends the new section to CHANGELOG.md, creating it if needed."""
    header = "# Changelog\n\nAll notable changes to this project will be documented here.\n\n"

    if os.path.exists(changelog_path):
        with open(changelog_path, "r") as f:
            existing = f.read()
        # Strip the header if present, we'll re-add it
        if existing.startswith("# Changelog"):
            existing = existing[existing.find("\n## "):]
        content = header + new_section + "\n\n" + existing.lstrip()
    else:
        content = header + new_section + "\n"

    with open(changelog_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    import sys
    version  = sys.argv[1] if len(sys.argv) > 1 else "Unreleased"
    from_ref = sys.argv[2] if len(sys.argv) > 2 else ""
    to_ref   = sys.argv[3] if len(sys.argv) > 3 else "HEAD"

    print(f"Generating changelog for {version} ({from_ref or 'beginning'}..{to_ref})")
    section = generate_changelog(version, from_ref, to_ref)
    prepend_to_changelog(section)
    print("CHANGELOG.md updated.")