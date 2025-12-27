# Project Structure

This document outlines the current, simplified structure of the project.

## 📂 File System

The project has been streamlined to use a single `main.py` for both local polling and cloud deployment. The `archive/` directory holds legacy files that are no longer in use.

```
.
├── main.py                          # Main application code for the bot.
├── deploy_cloud.sh                  # Deployment script for Google Cloud Functions.
├── requirements.txt                 # Python dependencies for the project.
├── .env.example                     # Example environment file for local development.
├── .gitignore                       # Specifies intentionally untracked files to ignore.
├── generate_diagram.py              # Script to generate architecture diagrams.
│
├── 📖 DOCUMENTATION
│   ├── README.md                    # Main project overview and setup guide.
│   ├── ENV_SETUP.md                 # Detailed guide for environment variable setup.
│   └── PROJECT_STRUCTURE.md         # This file.
│
└── 📦 ARCHIVE
    └── archive/                     # Contains numerous old and deprecated files.
```

---

## ✅ Essential Files

### Application Code
- **`main.py`**: The single source of truth for the bot's logic. It operates in two modes:
    - **Local Polling Mode**: Activated by setting the `FORCE_POLLING=true` environment variable.
    - **Webhook Mode**: The default mode when deployed to Google Cloud Functions.

### Deployment & Dependencies
- **`deploy_cloud.sh`**: The script used to deploy the application to Google Cloud Functions.
- **`requirements.txt`**: Contains all necessary Python packages, including `google-genai`, `pyTelegramBotAPI`, and `functions-framework`.

### Configuration
- **`.env.example`**: A template for the `.env` file, which is used for local development. Your `.env` file (which is gitignored) should contain your `TG_KEY` and `GEMINI_KEY`.
- **`.gitignore`**: Ensures that sensitive files (like `.env`) and unnecessary directories (like `.venv` and `__pycache__`) are not committed to version control.

### Documentation
- **`README.md`**: The primary guide for getting started with the project.
- **`ENV_SETUP.md`**: A detailed guide on how to set up your environment variables correctly.
- **`PROJECT_STRUCTURE.md`**: This file, providing an overview of the project's layout.

---

## 🎯 Development Workflow

1.  **Local Development**:
    *   Create and populate your `.env` file.
    *   Set the `FORCE_POLLING=true` environment variable.
    *   Run `python main.py` to test the bot locally.
2.  **Making Changes**:
    *   Modify `main.py` with your desired changes (e.g., update the `SYSTEM_PROMPT`).
3.  **Deploying Updates**:
    *   Run `./deploy_cloud.sh YOUR_PROJECT_ID YOUR_REGION` to deploy the latest version to the cloud. The script will use the credentials from your `.env` file.

This simplified structure makes the project easier to maintain and understand.