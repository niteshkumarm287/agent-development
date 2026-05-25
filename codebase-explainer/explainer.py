import os
import vertexai
from vertexai.generative_models import GenerativeModel
from pathlib import Path

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "game-d8160")
REGION     = os.environ.get("GCP_REGION", "us-central1")

vertexai.init(project=PROJECT_ID, location=REGION)
model = GenerativeModel("gemini-2.0-flash")

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv",
    "dist", "build", ".next", "vendor", "target",
}
CODE_EXTS = {
    ".py", ".js", ".ts", ".go", ".java", ".rs", ".rb",
    ".cpp", ".c", ".h", ".cs", ".swift", ".kt",
    ".yaml", ".yml", ".toml", ".json", ".env.example",
    ".md", ".txt", ".sh", ".dockerfile",
}
CONFIG_FILES = {
    "package.json", "pyproject.toml", "go.mod",
    "Cargo.toml", "pom.xml", "build.gradle",
    "Makefile", "docker-compose.yml", "Dockerfile",
    ".env.example", "README.md",
}

def estimate_tokens(text: str) -> int:
    """Rough estimate: 1 token ≈ 4 chars for code."""
    return len(text) // 4

def ingest_repo(repo_path: str, max_tokens: int = 800_000) -> tuple[str, dict]:
    """
    Reads repo files, prioritising config/entrypoints.
    Returns (concatenated_content, file_manifest).
    Stays within max_tokens to leave room for the prompt.
    """
    base = Path(repo_path)
    collected = []
    manifest  = {}
    total_tokens = 0

    # Pass 1: config + high-signal files first
    for fname in CONFIG_FILES:
        fpath = base / fname
        if fpath.exists():
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            tokens  = estimate_tokens(content)
            collected.append(f"### {fname}\n```\n{content[:6000]}\n```")
            manifest[fname] = {"tokens": tokens, "priority": "config"}
            total_tokens += tokens

    # Pass 2: all other code files, sorted by depth (shallower = higher priority)
    all_files = []
    for root, dirs, files in os.walk(base):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        depth   = Path(root).relative_to(base).parts.__len__()
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix.lower() in CODE_EXTS and fpath.name not in CONFIG_FILES:
                all_files.append((depth, fpath))

    all_files.sort(key=lambda x: x[0])

    for _, fpath in all_files:
        if total_tokens >= max_tokens:
            break
        rel = fpath.relative_to(base)
        try:
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            tokens  = estimate_tokens(content)
            cap     = min(len(content), 5000)
            collected.append(f"### {rel}\n```\n{content[:cap]}\n```")
            manifest[str(rel)] = {"tokens": tokens, "priority": "code"}
            total_tokens += tokens
        except Exception:
            continue

    return "\n\n".join(collected), manifest

PROMPTS = {
    "overview": """You are a senior engineer explaining a codebase to a non-technical stakeholder.

Given the source code below, write a clear plain-English explanation covering:
1. What this project does (1-2 sentences)
2. The problem it solves
3. Who would use it and why
4. The main technologies used
5. The most important files or modules (and what they do in plain English)

Use simple language. Avoid jargon. If you must use a technical term, explain it.
""",
    "architecture": """You are a senior software architect explaining a system to a new team member.

Given the source code below, explain the architecture:
1. High-level components and their responsibilities
2. How data flows through the system (entry point → processing → output)
3. Key design patterns or architectural decisions you can identify
4. External dependencies and why they're used
5. A simple text-based component diagram using ASCII art

Be specific — reference actual file names and function names where relevant.
""",
    "onboarding": """You are writing an onboarding guide for a developer joining this project today.

Given the source code below, write a practical getting-started guide:
1. Prerequisites (languages, tools, accounts needed)
2. How to run it locally (step by step)
3. The 3 most important files to read first, and why
4. How the main feature works end-to-end (trace one request/action through the code)
5. Common gotchas or things that tripped you up

Write as if you already know the codebase well. Be specific and practical.
""",
    "file": """You are a senior engineer doing a code review walkthrough.

Explain this file in plain English:
1. What is the purpose of this file?
2. What are the key functions/classes and what does each do?
3. What other parts of the codebase does it depend on?
4. What other parts depend on it?
5. Are there any non-obvious patterns or decisions worth noting?
""",
}

def explain(
    repo_path:   str,
    mode:        str = "overview",
    target_file: str = "",
) -> dict:
    """Main entrypoint. Returns explanation + metadata."""

    if mode == "file" and target_file:
        fpath = Path(repo_path) / target_file
        content = fpath.read_text(encoding="utf-8", errors="ignore")
        code_context = f"### {target_file}\n```\n{content}\n```"
        files_included = [target_file]
    else:
        code_context, manifest = ingest_repo(repo_path)
        files_included = list(manifest.keys())

    system_prompt = PROMPTS.get(mode, PROMPTS["overview"])

    full_prompt = f"""{system_prompt}

Source code:
{code_context}

Return only your explanation. No preamble like "Sure, here's..." or "Based on the code..."."""

    response = model.generate_content(full_prompt)

    return {
        "explanation":     response.text,
        "mode":            mode,
        "files_included":  len(files_included),
        "token_estimate":  estimate_tokens(code_context),
    }

if __name__ == "__main__":
    import sys, json
    repo   = sys.argv[1] if len(sys.argv) > 1 else "."
    mode   = sys.argv[2] if len(sys.argv) > 2 else "overview"
    target = sys.argv[3] if len(sys.argv) > 3 else ""
    result = explain(repo, mode, target)
    print(f"\n{'='*60}")
    print(f"Mode: {result['mode']} | Files: {result['files_included']} | ~{result['token_estimate']:,} tokens")
    print('='*60)
    print(result["explanation"])