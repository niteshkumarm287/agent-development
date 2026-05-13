# Automated README Generator

## One-line Description
An automated tool that leverages Google Generative AI to create and update `README.md` files for code repositories based on their content.

## Features
*   **AI-Powered Content Generation**: Utilizes Google's Gemini models through Vertex AI to intelligently summarize and describe project features, tech stack, and usage.
*   **Automated Workflow Integration**: Designed for seamless integration with CI/CD pipelines, specifically demonstrated with GitHub Actions for automatic README updates on pushes to the main branch.
*   **Configurable Scope**: Skips common development directories (e.g., `node_modules`, `.git`, `.venv`) and focuses on relevant source code files based on defined extensions.
*   **Project Contextualization**: Reads and processes repository source files to infer project purpose and generate accurate documentation.
*   **Concise and Professional Output**: Generates structured `README.md` files with essential sections.

## Tech Stack
*   **Python**: Core scripting language for the README generation logic.
*   **Google Generative AI (Vertex AI)**: Powers the content generation using large language models (specifically Gemini 2.5 Flash).
*   **GitHub Actions**: Automates the README generation and commit process.
*   **Google Cloud Platform**: Provides the underlying infrastructure for Vertex AI, including Workload Identity Federation for secure authentication.

## Prerequisites
*   **Python 3.x**: Installed on your system.
*   **Google Cloud Project**: An active GCP project with the Vertex AI API enabled.
*   **Service Account**: A Google Cloud service account with permissions to invoke Vertex AI models (e.g., `aiplatform.user`).
*   **Authentication**:
    *   For local development: Authenticated `gcloud` CLI or a service account key file.
    *   For GitHub Actions: Workload Identity Federation configured between your GitHub repository and Google Cloud.
*   **`requirements.txt`**: Ensure dependencies are listed and installed (e.g., `google-generativeai`, `google-auth`, `google-cloud-aiplatform`).

## Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Ensure `requirements.txt` includes `google-generativeai` and other necessary `google-cloud-*` packages if not already present).

## Usage
The `readme_gen.py` script can be run locally or integrated into a CI/CD pipeline. It generates a `README.md` file in the specified directory (defaults to the current directory).

### Environment Variables
The script relies on the following environment variables for Google Cloud authentication and model configuration:

*   `GCP_PROJECT_ID`: Your Google Cloud Project ID.
*   `GCP_REGION`: The GCP region where Vertex AI is enabled (e.g., `us-central1`, `global`).

### Example Commands

1.  **Run locally to generate `README.md` in the current directory:**
    ```bash
    export GCP_PROJECT_ID="your-gcp-project-id"
    export GCP_REGION="global" # Or your specific region
    python readme_gen.py .
    ```

2.  **Run locally to generate `README.md` for a specific path:**
    ```bash
    export GCP_PROJECT_ID="your-gcp-project-id"
    export GCP_REGION="global"
    python readme_gen.py /path/to/your/project
    ```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── readme.yml          # GitHub Actions workflow for automated README generation
├── readme_gen.py               # Main script for README generation
├── test.py                     # Example script demonstrating Google Generative AI client usage
└── gha-creds-0fed5ed62a212235.json # (Example) GCP service account credentials file structure
└── requirements.txt            # Python dependencies (assumed)
```

## Future Improvements
*   **Customizable Prompt Templates**: Allow users to define their own prompt structures and desired sections for the README.
*   **Configuration File Support**: Introduce a configuration file (e.g., `readme_gen.yaml`) for easier management of ignored directories, file extensions, and AI model parameters.
*   **Support for Multiple LLM Providers**: Extend functionality to work with other generative AI services (e.g., OpenAI, Anthropic).
*   **Interactive Mode**: Offer an interactive mode for users to review and refine generated content before saving.
*   **Advanced Content Extraction**: Implement more sophisticated parsing for common project files (e.g., `package.json`, `pom.xml`, `setup.py`) to extract dependencies and project metadata.
*   **Pre-commit Hook Integration**: Provide a pre-commit hook option to ensure the README is always up-to-date before commits.