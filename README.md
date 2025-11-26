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

4.  **Phase 4: Real LLM Strategy (Gemini API)**
    - Integrated Google's Gemini API to replace the mock LLM, enabling real intelligence for summarizing project threads and extracting actionable tasks.

5.  **Phase 5: Application Entry Point (main.py)**
    - (Upcoming) Wiring everything together into a runnable application.
