import argparse
import os
import sys
from dotenv import load_dotenv

from src.strategies.mongo_storage import MongoStorage
from src.strategies.gemini_llm import GeminiLLM
from src.strategies.cli_io import CliIO
from src.core.manager import ProjectManager

def main():
    # Load environment variables
    load_dotenv()

    # Check for critical configuration
    if not os.environ.get("MONGO_URI"):
        print("Error: MONGO_URI environment variable is not set.")
        print("Please check your .env file.")
        sys.exit(1)

    # Initialize strategies
    try:
        storage = MongoStorage()
        llm = GeminiLLM()
        io = CliIO()
    except Exception as e:
        print(f"Error initializing strategies: {e}")
        sys.exit(1)

    # Initialize manager
    manager = ProjectManager(storage=storage, llm=llm, io=io)

    # Setup argument parser
    parser = argparse.ArgumentParser(description="AI Project Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # daily-briefing command
    subparsers.add_parser("daily-briefing", help="Run daily briefing and dashboard")

    # add-log command
    add_log_parser = subparsers.add_parser("add-log", help="Add a log entry to a project")
    add_log_parser.add_argument("project", help="Project ID or Name")
    add_log_parser.add_argument("text", help="Log entry text")

    # check-stale command
    subparsers.add_parser("check-stale", help="Check for stale projects")

    # view-project command
    view_project_parser = subparsers.add_parser("view-project", help="View project details")
    view_project_parser.add_argument("project", help="Project ID or Name")

    # Parse arguments
    args = parser.parse_args()

    # Execute commands
    if args.command == "daily-briefing":
        manager.daily_briefing()
    elif args.command == "add-log":
        manager.add_log(args.project, args.text)
        print(f"Log added to project '{args.project}' and summary updated.")
    elif args.command == "check-stale":
        manager.check_stale_projects()
        print("Stale project check completed.")
    elif args.command == "view-project":
        manager.view_project(args.project)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
