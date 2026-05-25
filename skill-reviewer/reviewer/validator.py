import re

REQUIRED_SECTIONS = [
    "Description",
    "Examples",
    "Failure Cases"
]


def validate_skill(skill):
    issues = []
    content = skill["content"]

    for section in REQUIRED_SECTIONS:
        # Check for section existence
        section_header = f"# {section}"
        if section_header not in content:
            issues.append(f"Missing section: {section_header}")
            continue

        # Check for section content
        # Find the content between the current section and the next
        pattern = f"{section_header}(.*?)(?=\\n# |$)"
        match = re.search(pattern, content, re.DOTALL)

        if not match or not match.group(1).strip():
            issues.append(f"Empty section: {section_header}")

    return issues
