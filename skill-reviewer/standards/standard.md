# Skill Standards

This document outlines the standards for creating skills for this project.

## What is a Skill?

A skill is a self-contained unit of functionality. It is defined by a directory containing a `skill.md` file and an optional `metadata.yaml` file.

## File Structure

A skill directory must contain the following files:

*   `skill.md` (or `SKILL.md`): A markdown file that describes the skill.
*   `metadata.yaml` (optional): A YAML file containing metadata about the skill.

## `skill.md`

The `skill.md` file is the most important part of a skill. It must contain the following sections:

### # Description

A clear and concise description of what the skill does. This section should be easy to understand for someone who is not familiar with the skill.

### # Examples

A section containing examples of how to use the skill. This section should include at least one example.

### # Failure Cases

A section describing how the skill can fail. This section should include at least one example of a failure case.

## Example

Here is an example of a well-defined skill:

**skill.md**
```markdown
# Description

This skill greets the user.

# Examples

## Example 1: Greet the user by name

*   **Input**: "John"
*   **Output**: "Hello, John!"

# Failure Cases

## Failure Case 1: No name provided

*   **Input**: (empty)
*   **Output**: "Please provide a name."
```

**metadata.yaml**
```yaml
author: "John Doe"
version: "1.0.0"
```
