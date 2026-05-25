# Skill Reviewer

Skill Reviewer is a command-line tool for reviewing "skills". A skill is a directory containing a markdown file and an optional metadata file. The tool scans for skills, validates them against a set of rules, uses an AI to review them, and then calculates a score based on the validation and AI review.

## Installation

1.  Clone this repository.
2.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Set the `GEMINI_API_KEY` environment variable to your Gemini API key.

    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```

## Usage

To use the Skill Reviewer, run the `scan` command and provide a path to a skill directory or a directory containing multiple skill directories.

```bash
python -m reviewer.cli scan /path/to/skills
```

### Example

```bash
python -m reviewer.cli scan ./skills
```

This will scan the `skills` directory for valid skill directories and generate a report.

## How it Works

The Skill Reviewer uses a combination of static analysis and AI to review skills.

### Validation

The tool first validates the skill against a set of rules. These rules are defined in the `reviewer/validator.py` file. The current rules are:

*   The skill must have a `skill.md` or `SKILL.md` file.
*   The `skill.md` file must contain the following sections:
    *   `# Description`
    *   `# Examples`
    *   `# Failure Cases`
*   Each of these sections must have content.

### AI Review

After the skill is validated, the tool uses the Gemini API to review the skill's content. The AI is asked to rate the skill on a scale of 1-10 for the following criteria:

*   **Clarity**: Is the skill's purpose clear and easy to understand?
*   **Completeness**: Does the skill have all the necessary information?
*   **Maintainability**: Is the skill easy to update and maintain?
*   **Ambiguity**: Is the language unambiguous and precise?

The prompt used for the AI review is in the `reviewer/ai_reviewer.py` file.

### Scoring

The final score is calculated based on the validation issues and the AI review. The scoring logic is in the `reviewer/scorer.py` file.

*   Each validation issue deducts 20 points.
*   The AI review can add or deduct points based on the average rating.
*   A high ambiguity rating from the AI will deduct points.

## Skill Standards

For more information on what a good skill looks like, see the [Skill Standards](standards/standard.md) document.
