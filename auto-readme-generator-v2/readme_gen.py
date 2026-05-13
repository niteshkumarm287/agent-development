import os
from google import genai

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "game-d8160")
REGION = os.environ.get("GCP_REGION", "global")

MODEL_NAME = "gemini-2.5-flash"

print(f"PROJECT: {PROJECT_ID}")
print(f"REGION: {REGION}")
print(f"MODEL: {MODEL_NAME}")

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=REGION,
)

SKIP_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "dist",
    "build",
}

EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".go",
    ".java",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".md",
    ".sh",
}

def read_repo_files(repo_path: str, max_files: int = 20) -> str:
    collected = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            # Skip generated README
            if fname.lower() == "readme.md":
                continue
            if any(fname.endswith(ext) for ext in EXTENSIONS):
                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, repo_path)
                try:
                    with open(
                        fpath,
                        "r",
                        encoding="utf-8",
                        errors="ignore",
                    ) as f:
                        content = f.read()[:3000]
                    collected.append(
                        f"### {rel_path}\n"
                        f"```\n{content}\n```"
                    )
                except Exception as e:
                    print(f"Skipping {fpath}: {e}")
            if len(collected) >= max_files:
                break
    return "\n\n".join(collected)

def generate_readme(repo_path: str = ".") -> str:
    code_context = read_repo_files(repo_path)
    prompt = f"""
You are a senior technical writer.

Generate a professional README.md for this repository.

Sections to include:
- Project Name
- One-line Description
- Features
- Tech Stack
- Prerequisites
- Installation
- Usage
- Example Commands
- Project Structure
- Future Improvements

Instructions:
- Use proper markdown formatting
- Keep it concise but professional
- Infer project purpose from source code
- Return ONLY markdown
- No explanations
- No surrounding code fences

Source Code:
{code_context}
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text

if __name__ == "__main__":
    import sys
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    print("Generating README...")
    readme_content = generate_readme(repo_path)
    output_path = os.path.join(repo_path, "README.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"README generated successfully: {output_path}")