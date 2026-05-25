import subprocess
import json
import re
import logging

logger = logging.getLogger(__name__)


def extract_json(text):
    match = re.search(r'```json\n(\{.*?\})\n```', text, re.DOTALL)
    if match:
        return match.group(1)
    
    match = re.search(r'(\{.*?\})', text, re.DOTALL)
    if match:
        return match.group(1)

    return "{}"


def review_with_ai(content):
    prompt = f"""
Review this skill definition and rate it on a scale of 1-10 for the following criteria:
- **Clarity**: Is the skill's purpose clear and easy to understand?
- **Completeness**: Does the skill have all the necessary information?
- **Maintainability**: Is the skill easy to update and maintain?
- **Ambiguity**: Is the language unambiguous and precise?

Return ONLY a valid JSON object with the keys "clarity", "completeness", "maintainability", and "ambiguity".

**Skill Content:**
```markdown
{content}
```
"""

    try:
        result = subprocess.run(
            ['gemini', '--prompt', prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            logger.error(f"Gemini CLI failed: {result.stderr}")
            raise Exception(f"Gemini CLI error: {result.stderr}")
        
        cleaned = extract_json(result.stdout)
        return json.loads(cleaned)
    except subprocess.TimeoutExpired:
        logger.error("Gemini CLI timed out")
        return {
            "clarity": 5,
            "completeness": 5,
            "maintainability": 5,
            "ambiguity": 5,
            "error": "Gemini CLI timed out"
        }
    except Exception as e:
        logger.error(f"Error during AI review: {e}")
        return {
            "clarity": 5,
            "completeness": 5,
            "maintainability": 5,
            "ambiguity": 5,
            "error": f"Failed to get AI review: {str(e)}"
        }
