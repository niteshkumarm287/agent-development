# Changelog Generator

AI-powered changelog generator that uses Google Vertex AI (Gemini) to transform git commit history into clean, human-readable changelog entries.

## Overview

This tool analyzes git commits between tags/refs and generates changelog entries following the [Keep a Changelog](https://keepachangelog.com) format. It groups commits by Conventional Commits types and uses AI to rewrite technical commit messages into user-facing descriptions.

## Setup

### Prerequisites
- Python 3.8+
- Git repository
- Google Cloud Platform account with Vertex AI API enabled
- GCP credentials configured

### Installation

```bash
pip install -r requirements.txt
```

### Environment Variables

```bash
export GCP_PROJECT_ID="your-project-id"  # Default: game-d8160
export GCP_REGION="us-central1"          # Default: us-central1
```

## Usage

### Basic Usage

```bash
# Generate changelog from last tag to HEAD
python changelog_gen.py "v1.2.0"

# Generate from specific ref
python changelog_gen.py "v1.2.0" "v1.1.0"

# Generate between specific refs
python changelog_gen.py "v1.2.0" "v1.1.0" "main"
```

### Parameters

1. **version** (required): Version number for the changelog entry
2. **from_ref** (optional): Starting git ref (tag/branch/commit). Defaults to latest tag
3. **to_ref** (optional): Ending git ref. Defaults to HEAD

### Output

The script automatically:
- Generates AI-enhanced changelog entry
- Prepends it to `CHANGELOG.md` (creates if doesn't exist)
- Groups changes by: Added, Changed, Deprecated, Removed, Fixed, Security

### Commit Message Format

Works best with [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` → Added
- `fix:` → Fixed
- `docs:` → Documentation updates
- `chore:` → Maintenance
- `refactor:` → Code improvements
- `perf:` → Performance improvements
- `test:` → Testing

## Troubleshooting

**Authentication errors**: Ensure GCP credentials are configured (`gcloud auth application-default login`)

**No changes found**: Verify git refs exist and contain commits

**Model errors**: Check Vertex AI API is enabled and region supports gemini-2.5-flash
