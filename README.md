# AI Project Tracker

## Overview
A Python-based multi-agent project tracker designed to manage project states, logs, and summaries using advanced LLM strategies.

## 📝 Vibe Coding Workflow

This project was built using a prompt-driven, meta-management process. The development followed a unique workflow where the human developer acted as a high-level manager, providing strategic prompts, while the Antigravity IDE agent handled all implementation details, including file creation, modification, saving, and Git synchronization.

### Key Phases of Development

1.  **Phase 1: Core Abstractions & Interfaces**
    - Defined the foundational data models (`Project`, `Task`, `LogEntry`) and abstract base classes (`StorageStrategy`, `LLMStrategy`, `IOStrategy`) to enforce the Strategy Pattern.

2.  **Phase 2: Concrete Infrastructure Strategies**
    - Implemented concrete strategies for MongoDB storage, CLI-based IO using `rich`, and a Mock LLM for initial testing.

3.  **Phase 3: Core Manager Logic**
    - Developed the `ProjectManager` class to coordinate strategies, implementing business logic for "Rolling Summaries" and stale project detection.

    - Integrated Google's Gemini API to replace the mock LLM, enabling real intelligence for summarizing project threads and extracting actionable tasks.

5.  **Phase 5: Application Entry Point (main.py)**
    - Implemented `main.py` to wire everything together into a runnable application.

## 🚀 Usage

The application is run via the `main.py` entry point. Ensure your virtual environment is active (`source venv/bin/activate`) and your `.env` file is configured.

### Commands

#### 1. Daily Briefing
Runs the daily dashboard, checking for stale projects and displaying active ones.
```bash
python main.py daily-briefing
```

#### 2. Add Log
Adds a log entry to a project. If the project doesn't exist, it will be created. The LLM will automatically generate/update the project summary.
```bash
python main.py add-log <project_name_or_id> "Your log message here"
```
Example:
```bash
python main.py add-log "Website Redesign" "Completed the homepage layout using CSS Grid."
```

#### 3. Check Stale Projects
Manually triggers the stale project check (updates status to WARNING > 3 days, STALE > 7 days).
```bash
python main.py check-stale
```
